#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Young_Witch """
# pylint: disable=no-member, protected-access

import unittest
import random
from dominion import Card, Game, Piles


###############################################################################
class Card_YoungWitch(Card.Card):
    """Young Witch"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+2 Cards, Discard 2 cards. Each other player may reveal
            a Bane card from his hand. If he doesn't, he gains a Curse."""
        self.required_cards = ["Curse"]
        self.name = "Young Witch"
        self.cards = 2
        self.cost = 4

    def setup(self, game):
        """Setup: Add an extra Kingdom card pile costing 2 or 3 to the Supply.
        Cards from that pile are Bane cards."""
        banes = []
        for klass in game.cardmapping["Card"].values():
            card = klass()
            if card.name in game:
                continue
            if not card.insupply or not card.purchasable:
                continue
            if card.name in game.badcards:
                continue
            if card.cost in (2, 3):
                banes.append(card.name)
        game._bane = random.choice(banes)
        game._use_card_pile(game.getAvailableCards(), game._bane)
        game.output(f"Using {game._bane} as the bane for Young Witch")

    def special(self, game, player):
        player.plr_discard_cards(num=2, force=True)
        for pl in player.attack_victims():
            if pl.piles[Piles.HAND][game._bane]:
                player.output(f"{pl.name} has the bane: {game._bane}")
                continue
            player.output(f"{pl.name} got cursed")
            pl.output(f"{player.name}'s Young Witch cursed you")
            pl.gain_card("Curse")


###############################################################################
class TestYoungWitch(unittest.TestCase):
    """Test Young Witch"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Young Witch"],
            badcards=["Secret Chamber", "Duchess", "Caravan Guard"],
        )
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.card = self.g["Young Witch"].remove()

    def test_play_nobane(self):
        """Play the young witch without a bane"""
        self.victim.piles[Piles.HAND].set("Copper", "Silver")
        self.attacker.piles[Piles.HAND].set(
            "Copper", "Silver", "Gold", "Duchy", "Province"
        )
        self.attacker.add_card(self.card, Piles.HAND)
        self.attacker.test_input = ["Duchy", "Province", "finish"]
        self.attacker.play_card(self.card)
        try:
            bane = self.g.get_card_from_pile(self.g._bane)
            self.assertIn(bane.cost, (2, 3))
            self.assertEqual(self.attacker.piles[Piles.HAND].size(), 5 + 2 - 2)
            self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            print(f"Bane={self.g._bane}")
            self.g.print_state()
            raise

    def test_play_bane(self):
        """Play the young witch with a bane"""
        self.victim.piles[Piles.HAND].set("Copper", "Silver", self.g._bane)
        self.attacker.piles[Piles.HAND].set(
            "Copper", "Silver", "Gold", "Duchy", "Province"
        )
        self.attacker.add_card(self.card, Piles.HAND)
        self.attacker.test_input = ["Duchy", "Province", "finish"]
        self.attacker.play_card(self.card)
        try:
            self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            print(f"Bane={self.g._bane}")
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
