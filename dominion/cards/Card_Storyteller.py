#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Storyteller """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Storyteller(Card.Card):
    """Storyteller"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Action, +1 Coin; Play up to 3 Treasures from your hand.
            Pay all of your Coins; +1 Card per Coin paid"""
        self.name = "Storyteller"
        self.actions = 1
        self.coin = 1
        self.cost = 5

    def special(self, game, player):
        treasures = [_ for _ in player.hand if _.isTreasure()]
        if not treasures:
            return
        toplay = player.card_sel(
            num=3,
            cardsrc=treasures,
            prompt="Play 3 treasures to convert coin to cards",
            verbs=("Play", "Unplay"),
        )
        for card in toplay:
            player.play_card(card)
        player.output(f"Converting {player.coins.get()} coin to cards")
        player.pickup_cards(player.coins.get())
        player.coins.set(0)


###############################################################################
class Test_Storyteller(unittest.TestCase):
    """Test Storyteller"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Storyteller"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Storyteller"].remove()

    def test_play(self):
        """Play a Storyteller"""
        self.plr.hand.set("Copper", "Copper", "Silver", "Gold")
        self.plr.test_input = ["1", "2", "silver", "finish"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        # 1 from existing, 1 + story, 2 for two coppers and 2 for a silver
        self.assertEqual(self.plr.hand.size(), 1 + 1 + 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
