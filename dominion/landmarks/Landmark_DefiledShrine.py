#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Defiled_Shrine"""
import unittest
from dominion import Card, Game, Landmark, Player


###############################################################################
class Landmark_DefiledShrine(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When you gain an Action, move 1VP from its pile to this.
        When you buy a Curse, take the VP from this."""
        self.name = "Defiled Shrine"
        self.required_cards = ["Curse"]
        self.stored_vp = 0

    @classmethod
    def setup(cls, game: "Game.Game") -> None:
        cls._vp: dict[str, int] = {}
        for name, _ in game.get_card_piles():
            card = game.card_instances[name]
            if card and not card.isGathering():
                cls._vp[name] = 2

    def hook_all_players_buy_card(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: Card.Card,
    ) -> None:
        if game.landmarks["Defiled Shrine"]._vp[card.name]:
            game.landmarks["Defiled Shrine"]._vp[card.name] -= 1
            self.stored_vp += 1

    def hook_buy_card(
        self, game: "Game.Game", player: "Player.Player", card: Card.Card
    ) -> None:
        if card.name == "Curse":
            player.add_score("Defiled Shrine", self.stored_vp)
            self.stored_vp = 0


###############################################################################
class TestDefiledShrine(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2,
            landmarks=["Defiled Shrine"],
            initcards=["Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_use(self) -> None:
        """Use Defiled Shrine"""
        self.plr.buys.set(2)
        self.plr.coins.set(5)
        self.assertEqual(self.g.landmarks["Defiled Shrine"]._vp["Moat"], 2)
        self.plr.buy_card("Moat")
        self.assertEqual(self.g.landmarks["Defiled Shrine"]._vp["Moat"], 1)
        self.plr.buy_card("Curse")
        self.assertEqual(self.plr.score["Defiled Shrine"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
