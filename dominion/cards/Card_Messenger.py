#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, Phase, NoCardException


###############################################################################
class Card_Messenger(Card.Card):
    """Messenger"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Messenger"
        self.buys = 1
        self.coin = 2
        self.cost = 4

    def dynamic_description(self, player: Player.Player) -> str:
        """Variable description"""
        if player.phase == Phase.BUY:
            return """+1 Buy, +2 Coin, You may put your deck into your discard pile;
                When this is your first buy in a turn, gain a card costing up to 4,
                and each other player gains a copy of it."""
        return "+1 Buy, +2 Coin, You may put your deck into your discard pile"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if player.plr_choose_options(
            "Put entire deck into discard pile?",
            ("No - keep it as it is", False),
            ("Yes - dump it", True),
        ):
            for crd in player.piles[Piles.DECK]:
                player.add_card(crd, "discard")
                player.piles[Piles.DECK].remove(crd)

    def hook_buy_this_card(self, game: Game.Game, player: Player.Player) -> None:
        if len(player.stats["bought"]) != 1:
            return
        crd = player.plr_gain_card(4, prompt="Pick a card for everyone to gain")
        if not crd:
            return
        for plr in game.player_list():
            if plr != player:
                try:
                    plr.gain_card(crd.name)
                    plr.output(f"Gained a {crd.name} from {player}'s Messenger")
                except NoCardException:
                    player.output(f"No more {crd.name}s")


###############################################################################
class TestMessenger(unittest.TestCase):
    """Test Messenger"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Messenger"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Messenger")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Messenger - do nothing"""
        self.plr.test_input = ["No"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_discard(self) -> None:
        """Play a messenger and discard the deck"""
        deck_size = self.plr.piles[Piles.DECK].size()
        self.plr.test_input = ["Yes"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 0)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), deck_size)

    def test_buy(self) -> None:
        """Buy a messenger"""
        self.plr.test_input = ["get silver"]
        self.plr.coins.set(4)
        self.plr.buy_card("Messenger")
        for plr in self.g.player_list():
            self.assertIn("Silver", plr.piles[Piles.DISCARD])
            ag = plr.piles[Piles.DISCARD]["Silver"]
            self.assertEqual(ag.player.name, plr.name)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
