#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Order_of_Astrologers"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, Player, PlayArea

ASTROLOGERS = "astrologers"


###############################################################################
class Ally_Order_Astrologers(Ally.Ally):
    """Order of Astrologers"""

    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When shuffling, you may pick one card per Favor you spend to go on top."""
        self.name = "Order of Astrologers"

    def hook_pre_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """Players pick card to put on top"""
        if player.favors.get() == 0:
            return
        if ASTROLOGERS not in player.specials:
            player.specials[ASTROLOGERS] = PlayArea.PlayArea(name="Astrologers", initial=[])

        while player.favors.get() > 0:
            choices: list[tuple[str, Any]] = [("Do nothing", None)]
            names: set[str] = set()
            for card in player.piles[Piles.DISCARD]:
                if card.name in names:
                    continue
                names.add(card.name)
                choices.append((f"Put {card} on top", card))
            if choice := player.plr_choose_options("Spend a favor to put card on top? ", *choices):
                player.move_card(choice, player.specials[ASTROLOGERS])
                player.secret_count += 1
                player.favors.add(-1)
            else:
                break

    def hook_post_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """Put selected cards on top"""
        for card in player.specials.get(ASTROLOGERS, []):
            player.move_card(card, Piles.TOPDECK)
            player.secret_count -= 1
            player.specials[ASTROLOGERS].remove(card)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """Bots just don't use astrologers - they know better"""
    return None


###############################################################################
class Test_Order_Astrologers(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, allies="Order of Astrologers", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_one(self):
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DISCARD].set("Estate", "Duchy", "Province", "Estate", "Duchy", "Estate", "Duchy")
        self.plr.favors.set(1)
        self.plr.test_input = ["Put Province"]
        self.plr.end_turn()
        self.assertEqual(self.plr.favors.get(), 0)
        self.assertIn("Province", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
