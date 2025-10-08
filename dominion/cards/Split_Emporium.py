#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Emporium"""
import unittest

from dominion import Card, Game, Piles, Player, OptionKeys, Phase


###############################################################################
class Card_Emporium(Card.Card):
    """Emporium"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Emporium"
        self.coin = 1
        self.actions = 1
        self.cards = 1
        self.cost = 5
        self.pile = "Patrician"

    ###########################################################################
    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.ACTION:
            return "+1 Card, +1 Action, +1 Coin"
        return "+1 Card, +1 Action, +1 Coin. When you gain this, if you have at least 5 Action cards in play, +2VP."

    ###########################################################################
    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        count = sum(1 for _ in player.piles[Piles.PLAYED] if _.isAction())
        if count >= 5:
            player.add_score("Emporium", 2)
            player.output("Gained 2VP from Emporium")
        else:
            player.output(f"No VP as only have {count} action cards in play")
        return {}


###############################################################################
class Test_Emporium(unittest.TestCase):
    """Test Emporium"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Patrician", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Patrician", "Emporium")

    def test_play(self) -> None:
        """Play the Emporium"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_gain_with_actions(self) -> None:
        """Play the Emporium having played lots of actions"""
        self.plr.piles[Piles.PLAYED].set("Moat", "Moat", "Moat", "Moat", "Moat")
        for _ in range(6):  # Get the Patricians off the top of the stack
            self.plr.gain_card("Emporium")
        self.assertEqual(self.plr.get_score_details()["Emporium"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
