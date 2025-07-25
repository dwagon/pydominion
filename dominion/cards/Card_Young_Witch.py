#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Young_Witch"""
# pylint: disable=no-member, protected-access

import unittest
import random
from dominion import Card, Game, Piles, Keys, Player, NoCardException, game_setup

BANE = "young witch bane"


###############################################################################
class Card_YoungWitch(Card.Card):
    """Young Witch"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+2 Cards, Discard 2 cards. Each other player may reveal
            a Bane card from his hand. If he doesn't, he gains a Curse."""
        self.required_cards = ["Curse"]
        self.name = "Young Witch"
        self.cards = 2
        self.cost = 4

    def setup(self, game: Game.Game) -> None:
        """Setup: Add an extra Kingdom card pile costing 2 or 3 to the Supply.
        Cards from that pile are Bane cards."""
        banes = []
        for klass in game.card_mapping["Card"].values():
            card = klass()

            if card.name in game.card_piles.keys():
                continue
            if not card.insupply or not card.purchasable:
                continue
            if card.name in game.init[Keys.BAD_CARDS]:
                continue
            if card.cost not in (2, 3):
                continue
            banes.append(card.name)
        bane = random.choice(banes)
        game.specials[BANE] = bane
        game.use_card_pile(game.getAvailableCards(), game.specials[BANE])
        game.check_card_requirement(game.card_instances[bane])
        game.card_piles[bane].setup(game=game)
        if game.hexes or game.boons:
            game_setup.load_states(game)
        game.output(f"Using {bane} as the bane for Young Witch")

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.plr_discard_cards(num=2, force=True)
        for victim in player.attack_victims():
            if victim.piles[Piles.HAND][game.specials[BANE]]:
                player.output(f"{victim} has the bane: {game.specials[BANE]}")
                continue
            player.output(f"{victim} got cursed")
            victim.output(f"{player}'s Young Witch cursed you")
            try:
                victim.gain_card("Curse")
            except NoCardException:
                player.output("No more Curses")


###############################################################################
class TestYoungWitch(unittest.TestCase):
    """Test Young Witch"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Young Witch"],
            badcards=["Secret Chamber", "Duchess", "Caravan Guard"],
        )
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Young Witch")

    def test_play_nobane(self) -> None:
        """Play the young witch without a bane"""
        self.victim.piles[Piles.HAND].set("Copper", "Silver")
        self.attacker.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Duchy", "Province")
        self.attacker.add_card(self.card, Piles.HAND)
        self.attacker.test_input = ["Duchy", "Province", "finish"]
        self.attacker.play_card(self.card)
        try:
            bane = self.g.get_card_from_pile(self.g.specials[BANE])
            self.assertIn(bane.cost, (2, 3))
            self.assertEqual(self.attacker.piles[Piles.HAND].size(), 5 + 2 - 2)
            self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            print(f"Bane={self.g.specials[BANE]}")
            self.g.print_state()
            raise

    def test_play_bane(self) -> None:
        """Play the young witch with a bane"""
        self.victim.piles[Piles.HAND].set("Copper", "Silver", self.g.specials[BANE])
        self.attacker.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Duchy", "Province")
        self.attacker.add_card(self.card, Piles.HAND)
        self.attacker.test_input = ["Duchy", "Province", "finish"]
        self.attacker.play_card(self.card)
        try:
            self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            print(f"Bane={self.g.specials[BANE]}")
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
