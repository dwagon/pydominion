#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Riverboat"""
import random
import unittest
from typing import Any

from dominion import Game, Card, Player, OptionKeys, game_setup, Keys, Piles

RIVERBOAT = "riverboat"


###############################################################################
class Card_Riverboat(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.RISING_SUN
        self.name = "Riverboat"
        self.cost = 3

    def dynamic_description(self, player: "Player.Player") -> str:
        card_name = player.game.specials[RIVERBOAT]
        desc = player.game.card_instances[card_name].description(player)
        return f"At the start of your next turn, play {card_name}, leaving it there. ({card_name}: {desc})"

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """Play the set aside card, leaving it there."""
        player.output(f"Playing {game.specials[RIVERBOAT]} from Riverboat")
        player.card_benefits(game.card_instances[game.specials[RIVERBOAT]])
        # Try and handle cards that move themselves when played
        if game.card_instances[game.specials[RIVERBOAT]].location:
            player.remove_card(game.card_instances[game.specials[RIVERBOAT]])
            game.card_instances[game.specials[RIVERBOAT]].location = None
        return {}

    def setup(self, game: Game.Game) -> None:
        """Set aside an unused non-Duration Action card costing $5."""
        card = self.pick_card(game)
        self.setup_riverboat(game, card)

    def pick_card(self, game: Game.Game) -> str:
        """Pick suitable card to set aside"""
        actions = []
        for klass in game.card_mapping["Card"].values():
            card = klass()

            if card.name in game.card_piles.keys():
                continue
            if not card.insupply or not card.purchasable:
                continue
            if card.name in game_setup.INIT_CARDS[Keys.BAD_CARDS]:
                continue
            if card.isDuration() or not card.isAction():
                continue
            if card.cost != 5:
                continue
            actions.append(card.name)
        set_aside = random.choice(actions)
        return set_aside

    def setup_riverboat(self, game: Game.Game, set_aside: str):
        """Separate function so we can call it with named card for testing"""
        game.specials[RIVERBOAT] = set_aside
        game.card_instances[set_aside] = game.card_mapping["Card"][set_aside]()
        game_setup.check_card_requirement(game, game.card_instances[set_aside])
        game.output(f"Using {set_aside} as the card for Riverboat")


###############################################################################
class Test_Riverboat(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Riverboat"], badcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Riverboat")
        self.card.setup_riverboat(self.g, "Moat")  # type: ignore

    def test_pick_card(self) -> None:
        card_name = self.card.pick_card(self.g)  # type: ignore
        card = self.g.card_mapping["Card"][card_name]()
        self.assertEqual(card.cost, 5)
        self.assertFalse(card.isDuration())
        self.assertTrue(card.isAction())

    def test_play(self) -> None:
        """Play card"""
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 2)  # 2 for Moat


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
