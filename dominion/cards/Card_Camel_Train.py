#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Camel_Train """

import unittest
from dominion import Card, Game, Piles, Player, Phase


###############################################################################
class Card_Camel_Train(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Camel Train"
        self.cost = 3

    def dynamic_description(self, player: "Player.Player") -> str:
        if player.phase == Phase.BUY:
            return """Exile a non-Victory card from the Supply. When you gain this, Exile a Gold from the Supply."""
        return "Exile a non-Victory card from the Supply."

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        options = []
        for name, pile in game.get_card_piles():
            if pile.is_empty():
                continue
            card = game.card_instances[name]
            if card.isVictory():
                continue
            if not card.purchasable:
                continue
            options.append((f"Exile {name}", name))

        if to_exile := player.plr_choose_options("Pick a card to Exile", *options):
            player.exile_card_from_supply(to_exile)

    def hook_gain_this_card(self, game: "Game.Game", player: "Player.Player") -> None:
        player.exile_card_from_supply("Gold")


###############################################################################
class TestCamelTrain(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Camel Train"], badcards=["Silver Mine"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Camel Train")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        self.plr.test_input = ["Exile Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.EXILE])

    def test_gain(self) -> None:
        self.plr.gain_card("Camel Train")
        self.assertIn("Gold", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
