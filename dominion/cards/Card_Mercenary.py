#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Mercenary(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """You may trash 2 cards from your hand.
        If you do, +2 Cards, +2 Coin, and each other player discards down to 3 cards in hand."""
        self.name = "Mercenary"
        self.insupply = False
        self.purchasable = False
        self.cost = 0

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may trash 2 cards from your hand. If you do, +2
        cards, +2 coin, and each other player discards down to 3
        cards in hand"""

        ans = player.plr_choose_options(
            "Trash cards?", ("Trash nothing", False), ("Trash 2 cards", True)
        )
        if not ans:
            return
        player.plr_trash_card(2, force=True)
        player.pickup_cards(2)
        player.coins.add(2)
        for plr in player.attack_victims():
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Mercenary(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Urchin", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Mercenary")

    def test_play(self) -> None:
        """Trash nothing with mercenary - should do nothing"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())

    def test_defense(self) -> None:
        """Make sure moats work against mercenaries"""
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        moat = self.g.get_card_from_pile("Moat")
        self.victim.add_card(moat, Piles.HAND)
        self.plr.test_input = ["1", "1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        # 5 for hand + moat
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 6)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())

    def test_attack(self) -> None:
        """Attack with a mercenary"""
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1", "1", "2", "0"]
        self.victim.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
