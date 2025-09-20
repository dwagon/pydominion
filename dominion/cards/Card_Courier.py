#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Courier"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Courier(Card.Card):
    """Courier"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.desc = """+$1; Discard the top card of your deck. Look through your discard pile;
        you may play an Action or Treasure from it."""
        self.name = "Courier"
        self.coin = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Discard the top card of your deck. Look through your discard pile;
        you may play an Action or Treasure from it."""
        try:
            top_card = player.next_card()
        except NoCardException:
            return
        player.output(f"Discard {top_card}")
        player.discard_card(top_card)
        action_treasures = [
            _ for _ in player.piles[Piles.DISCARD] if _.isAction() or _.isTreasure()
        ]
        if not action_treasures:
            player.output("No suitable cards")
            return
        options = [(f"Play {_}: {_.desc}", _) for _ in action_treasures]
        options.insert(0, ("Do nothing", None))
        if to_play := player.plr_choose_options(
            "Courier can play a card from your discard", *options
        ):
            player.play_card(to_play, cost_action=False, discard=False)


###############################################################################
class TestCourier(unittest.TestCase):
    """Test Courier"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Courier"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Courier")

    def test_play(self) -> None:
        """Play a Courier"""
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.DISCARD].set("Estate", "Copper", "Silver", "Gold")
        coin = self.plr.coins.get()
        self.plr.test_input = ["Play Gold"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coin + 1 + 3)  # +1 Courier, +3 Gold
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
