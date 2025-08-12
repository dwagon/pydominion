#!/usr/bin/env python

import random
import unittest

from dominion import Card, Game, Prophecy, Player, OptionKeys, Piles, game_setup, Keys

ARMY_ATTACK = "army attack"


###############################################################################
class Prophecy_Approaching_Army(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "After you play an Attack card, +$1."
        self.name = "Approaching Army"

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        """After you play an Attack card, +$1."""
        if card.isAttack():
            player.coins.add(1)
        return {}

    def setup(self, game: Game.Game) -> None:
        """Setup: Add an extra Attack Kingdom card to the Supply."""
        attacks = []
        for klass in game.card_mapping["Card"].values():
            card = klass()

            if card.name in game.card_piles.keys():
                continue
            if not card.insupply or not card.purchasable:
                continue
            if card.name in game_setup.INIT_CARDS[Keys.BAD_CARDS]:
                continue
            if not card.isAttack():
                continue
            attacks.append(card.name)
        attack = random.choice(attacks)
        game.specials[ARMY_ATTACK] = attack
        game_setup.use_card_pile(game, game.getAvailableCards(), game.specials[ARMY_ATTACK])
        game_setup.check_card_requirement(game, game.card_instances[attack])
        game.card_piles[attack].setup(game=game)
        if game.hexes or game.boons:
            game_setup.load_states(game)
        game.output(f"Using {attack} as the attack card for Approaching Army")


###############################################################################
class Test_Approaching_Army(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, prophecies=["Approaching Army"], initcards=["Mountain Shrine", "Witch"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        card = self.g.get_card_from_pile("Witch")
        self.plr.add_card(card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(card)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.assertTrue(self.g.card_instances[self.g.specials[ARMY_ATTACK]].isAttack())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
