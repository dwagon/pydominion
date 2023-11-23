#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Smugglers(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Gain a copy of a card costing up to 6 that the player to your right gained on his last turn."""
        self.name = "Smugglers"
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        plr = game.playerToRight(player)
        if cards := [_ for _ in plr.stats["bought"] if _.cost <= 6]:
            if card := player.card_sel(cardsrc=cards):
                try:
                    player.gain_card(card[0].name)
                except NoCardException:
                    player.output(f"No more {card[0].name}")
        else:
            player.output(f"{plr} didn't buy any suitable cards")


###############################################################################
class Test_Smugglers(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Smugglers"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Smugglers")

    def test_play(self) -> None:
        """Play a smugglers"""
        self.other.stats["bought"] = [self.g.get_card_from_pile("Gold")]
        self.plr.test_input = ["gold"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
