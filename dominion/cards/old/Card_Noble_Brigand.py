#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Noble_Brigand(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.HINTERLANDS
        self.desc = """+1 Coin. When you buy this or play it, each other player reveals
            the top 2 cards of his deck, trashes a revealed Silver or Gold you choose,
            and discards the rest. If he didn't reveal a Treasure, he gains a Copper.
            You gain the trashed cards."""
        self.name = "Noble Brigand"
        self.coin = 1
        self.cost = 4

    def special(self, game, player):
        self.attack(game, player)

    def hook_buy_this_card(self, game, player):
        self.attack(game, player)

    def attack(self, game, player):
        for victim in player.attack_victims():
            cards = self.getTreasureCards(victim, player)
            if not cards:
                victim.output(f"{player.name}'s Noble Brigand gave you a copper")
                victim.gain_card("Copper")
                continue
            ans = None
            choices = []
            for card in cards:
                if card.name in ("Silver", "Gold"):
                    choices.append((f"Steal {card.name}", card))
            if choices:
                ans = player.plr_choose_options("Pick a card to steal", *choices)
            for card in cards:
                if card == ans:
                    victim.trash_card(card)
                    victim.output(f"{player.name}'s Noble Brigand trashed your {card.name}")
                    player.output(f"Stole {card.name} from {victim.name}")
                    game.trashpile.remove(ans)
                    card.player = player
                    player.add_card(ans)
                else:
                    victim.output(f"{player.name}'s Noble Brigand discarded your {card.name}")
                    victim.discard_card(card)

    @classmethod
    def getTreasureCards(cls, plr, player):
        cards = []
        for _ in range(2):
            c = plr.next_card()
            plr.reveal_card(c)
            if c.isTreasure():
                cards.append(c)
            else:
                plr.output(f"{player.name}'s Noble Brigand discarded your {c.name}")
                plr.add_card(c, "discard")
        return cards


###############################################################################
class Test_Noble_Brigand(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Noble Brigand"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Noble Brigand"].remove()

    def test_play(self):
        """Play an Noble Brigand but without anything to steal"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_no_treasure(self):
        """Play an Noble Brigand but with no treasure"""
        self.vic.deck.set("Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.vic.discardpile.size(), 3)
        self.assertIn("Copper", self.vic.discardpile)

    def test_gold(self):
        """Play an Noble Brigand with a gold"""
        self.vic.deck.set("Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.discardpile.size(), 1)
        self.assertIn("Silver", self.vic.discardpile)
        self.assertNotIn("Gold", self.vic.discardpile)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertNotIn("Gold", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
