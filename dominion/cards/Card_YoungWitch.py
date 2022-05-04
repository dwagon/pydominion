#!/usr/bin/env python
# pylint: disable=no-member

import unittest
import random
from dominion import Card, Game


###############################################################################
class Card_YoungWitch(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.CORNUCOPIA
        self.desc = """+2 Cards, Discard 2 cards. Each other player may reveal
            a Bane card from his hand. If he doesn't, he gains a Curse."""
        self.required_cards = ["Curse"]
        self.name = "Young Witch"
        self.cards = 2
        self.cost = 4

    def setup(self, game):
        """Setup: Add an extra Kingdom card pile costing 2 or 3 to the Supply. Cards from that pile are Bane cards."""
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
        game._use_cardpile(game.getAvailableCards(), game._bane)
        game.output(f"Using {game._bane} as the bane for Young Witch")

    def special(self, game, player):
        player.plr_discard_cards(num=2, force=True)
        for pl in player.attack_victims():
            if pl.in_hand(game._bane):
                player.output(f"{pl.name} has the bane: {game._bane}")
                continue
            player.output(f"{pl.name} got cursed")
            pl.output(f"{player.name}'s Young Witch cursed you")
            pl.gain_card("Curse")


###############################################################################
class Test_YoungWitch(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Young Witch"],
            badcards=["Secret Chamber", "Duchess", "Caravan Guard"],
            ally="Plateau Shepherds"
        )
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.card = self.g["Young Witch"].remove()

    def test_play_nobane(self):
        """Play the young witch without a bane"""
        self.victim.set_hand("Copper", "Silver")
        self.attacker.set_hand("Copper", "Silver", "Gold", "Duchy", "Province")
        self.attacker.add_card(self.card, "hand")
        self.attacker.test_input = ["Duchy", "Province", "finish"]
        self.attacker.play_card(self.card)
        try:
            self.assertIn(self.g[self.g._bane].cost, (2, 3))
            self.assertEqual(self.attacker.hand.size(), 5 + 2 - 2)
            self.assertIn("Curse", self.victim.discardpile)
        except AssertionError:  # pragma: no cover
            print(f"Bane={self.g._bane}")
            self.g.print_state()
            raise

    def test_play_bane(self):
        """Play the young witch with a bane"""
        self.victim.set_hand("Copper", "Silver", self.g._bane)
        self.attacker.set_hand("Copper", "Silver", "Gold", "Duchy", "Province")
        self.attacker.add_card(self.card, "hand")
        self.attacker.test_input = ["Duchy", "Province", "finish"]
        self.attacker.play_card(self.card)
        try:
            self.assertNotIn("Curse", self.victim.discardpile)
        except AssertionError:  # pragma: no cover
            print(f"Bane={self.g._bane}")
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
