#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Daimyo"""
import unittest

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Daimyo(Card.Card):
    """Daimyo"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.COMMAND]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = (
            """+1 Card; +1 Action; The next time you play a non-Command Action card this turn, replay it afterwards."""
        )
        self.name = "Daimyo"
        self.debtcost = 6
        self.cards = 1
        self.actions = 1

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        """The next time you play a non-Command Action card this turn, replay it afterwards."""
        if not card.isAction() or card.isCommand():
            return {}
        if player.do_once(self.uuid):
            player.output(f"Daimyo plays {card} again")
            player.play_card(card, discard=False, cost_action=False, post_action_hook=False)
        return {}


###############################################################################
class TestDaimyo(unittest.TestCase):
    """Test Daimyo"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Daimyo", "Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_action(self) -> None:
        """Test action"""
        # Test by playing mine twice on a copper. Cu -> Ag -> Au
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.piles[Piles.PLAYED].set("Daimyo")
        self.plr.test_input = ["Upgrade Copper", "Get Silver", "Upgrade Silver", "Get Gold"]
        mine = self.g.get_card_from_pile("Mine")
        self.plr.play_card(mine)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Mine", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Mine", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.actions.get(), 0)

    def test_non_action(self) -> None:
        """Test non-action"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.piles[Piles.PLAYED].set("Daimyo")
        gold = self.g.get_card_from_pile("Gold")
        self.plr.play_card(gold)

    def test_play(self) -> None:
        """Test play"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.piles[Piles.PLAYED].set("Daimyo")
        card = self.g.get_card_from_pile("Daimyo")
        actions = self.plr.actions.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(card)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)  # +1 for Card, -1 for playing it
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
