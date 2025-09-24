#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Order_of_Masons"""
import math
import unittest

from dominion import Card, Game, Piles, Ally, Player, PlayArea

MASONS = "Masons"


###############################################################################
class Ally_Order_Masons(Ally.Ally):
    """Order of Masons"""

    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When shuffling, you may pick up to 2 cards per Favor you spend to put into your discard pile."""
        self.name = "Order of Masons"

    def hook_pre_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """Players pick card to put on top"""
        if player.favors.get() == 0:
            return
        if MASONS not in player.specials:
            player.specials[MASONS] = PlayArea.PlayArea(name="Masons", initial=[])
        max_cards = player.favors.get() * 2
        if cards := player.card_sel(
            num=max_cards,
            cardsrc=Piles.DISCARD,
            prompt=f"Spend a favor per 2 to put cards (max {max_cards}) into discard pile? ",
        ):
            for card in cards:
                player.move_card(card, player.specials[MASONS])
                player.secret_count += 1
            cost = math.ceil(len(cards) / 2)
            player.output(f"Put {len(cards)} into discard so spending {cost} favors")

            player.favors.add(-cost)

    def hook_post_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """Put selected cards on discard"""
        for card in player.specials.get(MASONS, []):
            player.move_card(card, Piles.DISCARD)
            player.secret_count -= 1
            player.specials[MASONS].remove(card)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover pylint:disable=unused-argument
    """Bots just don't use Masons"""
    return None


###############################################################################
class Test_Order_Masons(unittest.TestCase):
    """Test Order of Masons"""

    def setUp(self) -> None:
        """Set up tests"""
        self.g = Game.TestGame(numplayers=1, allies="Order of Masons", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Use Order of Masons"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DISCARD].set("Estate", "Estate", "Province", "Estate", "Duchy", "Estate")
        self.plr.favors.set(3)
        self.plr.test_input = ["Select Province", "Select Duchy", "Finish"]
        self.plr.end_turn()
        self.assertEqual(self.plr.favors.get(), 2)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
