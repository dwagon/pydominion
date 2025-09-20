#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Storyteller"""

import unittest

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Storyteller(Card.Card):
    """Storyteller"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Action. Play up to 3 Treasures from your hand.
                Then, +1 Card, and pay all of your $ for +1 Card per $1 you paid."""
        self.name = "Storyteller"
        self.actions = 1
        self.cost = 5

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Play up to 3 Treasures from your hand. Then, +1 Card, and pay all of your $ for +1 Card per $1 you paid."""
        treasures = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treasures:
            return
        toplay = player.card_sel(
            num=3,
            cardsrc=treasures,
            prompt="Play up to 3 Treasures from your hand.",
            verbs=("Play", "Unplay"),
        )
        for card in toplay:
            player.play_card(card)
        player.pickup_cards(1)
        player.output(f"Converting {player.coins.get()} coin to cards")
        player.pickup_cards(player.coins.get())
        player.coins.set(0)


###############################################################################
class Test_Storyteller(unittest.TestCase):
    """Test Storyteller"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Storyteller"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Storyteller")

    def test_play(self) -> None:
        """Play a Storyteller"""
        self.plr.piles[Piles.HAND].set("Copper", "Copper", "Silver", "Gold")
        self.plr.test_input = ["1", "2", "silver", "finish"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        # 1 from existing, 1 + story, 2 for two coppers and 2 for a silver
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 1 + 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
