#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, OptionKeys, Phase


###############################################################################
class Card_Skulk(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK, Card.CardType.DOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Skulk"
        self.buys = 1
        self.cost = 4

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return "+1 Buy; Each other player receives the next Hex; When you gain this, gain a Gold."
        return "+1 Buy; Each other player receives the next Hex."

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.gain_card("Gold")
        return {}

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Skulk hexed you")
            plr.receive_hex()


###############################################################################
class Test_Skulk(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Skulk"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.skulk = self.g.get_card_from_pile("Skulk")
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_card(self) -> None:
        """Play Skulk"""
        self.plr.add_card(self.skulk, Piles.HAND)
        self.plr.play_card(self.skulk)
        self.assertTrue(self.vic.has_state("Deluded"))

    def test_gain(self) -> None:
        self.plr.gain_card("Skulk")
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
