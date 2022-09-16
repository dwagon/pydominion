#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_PirateShip(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Choose one: Each other player reveals the top 2 cards of his deck,
            trashes a revealed Treasure that you choose, discards the rest,
            and if anyone trashed a Treasure you take a Coin token;
            or, +1 per Coin token you've taken with Pirate Ships this game."""
        self.name = "Pirate Ship"
        self.cost = 4

    def special(self, game, player):
        choice = player.plr_choose_options(
            "Pick one",
            (
                "Each other player reveals the top 2 cards of his deck, trashes a "
                + "revealed Treasure that you choose, discards the rest, and if anyone "
                + "trashed a Treasure you take a Coin token",
                "attack",
            ),
            (
                "+%d = +1 per treasure you've taken with Pirate Ships this game."
                % player._pirate_ship,
                "spend",
            ),
        )
        if choice == "attack":
            trashed = False
            for victim in player.attack_victims():
                if self.attack_player(player, victim):
                    trashed = True
            if trashed:
                player._pirate_ship += 1
        else:
            player.coins.add(player._pirate_ship)

    def attack_player(self, player, victim):
        trashed = False
        cards = []
        for _ in range(2):
            card = victim.next_card()
            victim.reveal_card(card)
            if card.isTreasure():
                cards.append(card)
            else:
                victim.output("%s's Pirate Ship discarded your %s" % (player.name, card.name))
                victim.add_card(card, "discard")
        if cards:
            to_trash = player.plr_trash_card(
                prompt="Trash a card from %s" % victim.name, cardsrc=cards
            )
            trashed = True
            for card in cards:
                if card not in to_trash:
                    victim.add_card(card, "discard")
                    victim.output("Discarded %s" % card.name)
                else:
                    victim.output("Trashed %s" % card.name)
        else:
            player.output("Player %s has no treasures to trash" % victim.name)
        return trashed

    def hook_gain_this_card(self, game, player):
        if not hasattr(player, "_pirate_ship"):
            player._pirate_ship = 0
        return {}


###############################################################################
class Test_PirateShip(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Pirate Ship"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Pirate Ship"].remove()
        self.plr.gain_card(newcard=self.card, destination="hand")

    def test_play_attack(self):
        tsize = self.g.trashpile.size()
        self.vic.deck.set("Copper", "Estate")
        self.plr.test_input = ["Each other", "copper"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.g.trashpile.size(), tsize + 1)
            self.assertIn("Copper", self.g.trashpile)
            self.assertEqual(self.plr._pirate_ship, 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_trash_nothing(self):
        """Play the card but chose to not trash anything"""
        self.vic.deck.set("Copper", "Estate")
        self.plr.test_input = ["Each other", "Finish selecting"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.vic.discardpile)

    def test_spend(self):
        self.plr._pirate_ship = 2
        self.plr.test_input = ["per treasure"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
