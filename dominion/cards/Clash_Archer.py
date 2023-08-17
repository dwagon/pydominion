#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Archer """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Archer(Card.Card):
    """Archer"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.CLASH,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.name = "Archer"
        self.coins = 2
        self.desc = """+$2; Each other player with 5 or more cards in hand reveals all but one,
        and discards one of those you choose."""

    def special(self, game, player):
        """Each other player with 5 or more cards in hand reveals all but one,
        and discards one of those you choose."""
        for plr in player.attack_victims():
            if plr.piles[Piles.HAND].size() >= 5:
                self.attack(plr, player)

    def attack(self, victim, player):
        """Attack the victim"""
        victim.output(
            f"{player.name}'s Archer causes you to reveal all but one"
            " card from your hand - they can discard one of the cards you reveal"
        )
        hide = victim.card_sel(num=1, prompt="Select card to not reveal")
        cards = []
        for crd in victim.piles[Piles.HAND]:
            if crd == hide[0]:
                continue
            cards.append(crd)
            victim.reveal_card(crd)
        disc = player.card_sel(
            prompt=f"Discard a card from {victim.name}s hand", cardsrc=cards
        )
        victim.discard_card(disc[0])
        victim.output(f"Discarded {disc[0].name}")


###############################################################################
class TestArcher(unittest.TestCase):
    """Test Archer"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Clashes"], use_liaisons=True)
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play_archer(self):
        """Play an Archer"""
        while True:
            card = self.g["Clashes"].remove()
            if card.name == "Archer":
                break
        self.plr.add_card(card, Piles.HAND)
        self.vic.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.vic.test_input = ["Select Gold"]
        self.plr.test_input = ["Select Silver"]
        self.plr.play_card(card)
        self.assertIn("Silver", self.vic.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
