#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Oracle(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Each player (including you) reveals the top 2 cards of their deck, and discards them 
        or puts them back, your choice (they choose the order). Then, +2 Cards."""
        self.name = "Oracle"
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        for plr in player.attack_victims():
            self.attack(player, plr, f"{plr.name}'s")
        self.attack(player, player, "your")
        player.pickup_cards(2)

    def attack(
        self, player: "Player.Player", victim: "Player.Player", name: str
    ) -> None:
        """reveals the top 2 cards of their deck, and discards them or puts them back, your choice"""
        cards = []
        for _ in range(2):
            try:
                card = victim.next_card()
            except NoCardException:
                break
            victim.reveal_card(card)
            cards.append(card)
        card_names = ", ".join([_.name for _ in cards])
        discard = player.plr_choose_options(
            f"What to do with {name} cards: {card_names}",
            (f"Discard {card_names}", True),
            (f"Put {card_names} on top of deck", False),
        )
        if discard:
            for card in cards:
                victim.discard_card(card)
            victim.output(f"{player.name}'s Oracle discarded your {card_names}")
        else:
            for card in cards:
                victim.add_card(card, "topdeck")
            victim.output(
                f"{player.name}'s Oracle put {card_names} on top of your deck"
            )


###############################################################################
class TestOracle(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Oracle"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Oracle")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play Oracle"""
        self.vic.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.test_input = ["discard", "top"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.piles[Piles.DISCARD])
        self.assertIn("Province", self.vic.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
