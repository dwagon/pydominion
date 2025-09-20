#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Noble_Brigand(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+1 Coin. When you buy this or play it, each other player reveals
            the top 2 cards of his deck, trashes a revealed Silver or Gold you choose,
            and discards the rest. If he didn't reveal a Treasure, he gains a Copper.
            You gain the trashed cards."""
        self.name = "Noble Brigand"
        self.coin = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        self.attack(game, player)

    def hook_buy_this_card(self, game: Game.Game, player: Player.Player) -> None:
        self.attack(game, player)

    def attack(self, game: Game.Game, player: Player.Player) -> None:
        for victim in player.attack_victims():
            cards = self.get_treasure_cards(victim, player)
            if not cards:
                try:
                    victim.gain_card("Copper")
                    victim.output(f"{player}'s Noble Brigand gave you a copper")
                except NoCardException:
                    player.output("No more Coppers")
                continue
            ans = None
            choices = []
            for card in cards:
                if card.name in ("Silver", "Gold"):
                    choices.append((f"Steal {card}", card))
            if choices:
                ans = player.plr_choose_options("Pick a card to steal", *choices)
            for card in cards:
                if card == ans:
                    victim.trash_card(card)
                    victim.output(f"{player}'s Noble Brigand trashed your {card}")
                    player.output(f"Stole {card} from {victim}")
                    game.trash_pile.remove(ans)
                    card.player = player
                    player.add_card(ans)
                else:
                    victim.output(f"{player}'s Noble Brigand discarded your {card}")
                    victim.discard_card(card)

    @classmethod
    def get_treasure_cards(
        cls, plr: Player.Player, player: Player.Player
    ) -> list[Card.Card]:
        cards = []
        for _ in range(2):
            try:
                card = plr.next_card()
            except NoCardException:
                break
            plr.reveal_card(card)
            if card.isTreasure():
                cards.append(card)
            else:
                plr.output(f"{player.name}'s Noble Brigand discarded your {card}")
                plr.add_card(card, Piles.DISCARD)
        return cards


###############################################################################
class TestNobleBrigand(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Noble Brigand"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Noble Brigand")

    def test_play(self) -> None:
        """Play a Noble Brigand but without anything to steal"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_no_treasure(self) -> None:
        """Play a Noble Brigand but with no treasure"""
        self.vic.piles[Piles.DECK].set("Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.vic.piles[Piles.DISCARD].size(), 3)
        self.assertIn("Copper", self.vic.piles[Piles.DISCARD])

    def test_gold(self) -> None:
        """Play a Noble Brigand with a gold"""
        self.vic.piles[Piles.DECK].set("Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Silver", self.vic.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.vic.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
