#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Secluded_Shrine"""
import unittest
from typing import Optional, Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_SecludedShrine(Card.Card):
    """Secluded Shrine"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "+$1; The next time you gain a Treasure, trash up to 2 cards from your hand."
        self.name = "Secluded Shrine"
        self.cost = 3
        self.coin = 1
        self.permanent = True

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> Optional[dict[OptionKeys, Any]]:
        if self.location != Piles.DURATION:
            return None
        if not card.isTreasure():
            return None
        if player.piles[Piles.HAND].size() == 0:
            return None
        player.plr_trash_card(
            num=2,
            cardsrc=Piles.HAND,
            prompt="Secluded Shrine lets you trash up to two cards",
        )
        player.move_card(self, Piles.DISCARD)
        return None


###############################################################################
class TestSecludedShrine(unittest.TestCase):
    """Test Secluded Shrine"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Secluded Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Secluded Shrine")

    def test_play(self) -> None:
        """Play a secluded shrine"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.test_input = ["Trash Copper", "Finish"]
        self.plr.gain_card("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
