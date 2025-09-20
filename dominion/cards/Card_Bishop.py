#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles


###############################################################################
class Card_Bishop(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 Coin, +1 VP; Trash a card from your hand. +VP equal
            to half its cost in coins, rounded down. Each other player may trash a
            card from his hand"""
        self.name = "Bishop"
        self.coin = 1
        self.victory = 1
        self.cost = 4

    def special(self, game, player):
        """Trash a card from your hand. +VP equal to half its cost
        in coins, rounded down. Each other player may trash a card
        from his hand"""
        for plr in game.player_list():
            if plr == player:
                self.trashOwnCard(player)
            else:
                self.trashOtherCard(player, plr)

    @classmethod
    def trashOwnCard(cls, player):
        tc = player.plr_trash_card(
            printcost=True, prompt="Gain VP worth half the cost of the card you trash"
        )
        if not tc:
            return
        card = tc[0]
        points = int(card.cost / 2)
        player.add_score("bishop", points)
        player.output(f"Trashing {card} for {points} points")

    @classmethod
    def trashOtherCard(cls, player, victim):
        victim.output(f"{player.name}'s bishop lets you trash a card")
        tc = victim.plr_trash_card()
        if tc:
            victim.output(f"Trashing {tc[0]}")
        else:
            victim.output("All mine I tell you, all mine")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Trash an estate, then a copper else nothing
    es = player.piles[Piles.HAND]["estate"]
    if es:
        return [es]
    cu = player.piles[Piles.HAND]["copper"]
    if cu:
        return [cu]
    return []


###############################################################################
class TestBishop(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Bishop"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.bishop = self.g.get_card_from_pile("Bishop")

    def test_play(self):
        self.plr.add_card(self.bishop, Piles.HAND)
        self.plr.test_input = ["finish"]
        self.other.test_input = ["finish"]
        self.plr.play_card(self.bishop)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_trash(self):
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.bishop, Piles.HAND)
        self.plr.test_input = ["trash gold"]
        self.other.test_input = ["finish"]
        self.plr.play_card(self.bishop)
        self.assertEqual(self.plr.score["bishop"], 3)
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.assertIn("Gold", self.g.trash_pile)

    def test_both_trash(self):
        trash_size = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold")
        self.other.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.bishop, Piles.HAND)
        self.plr.test_input = ["trash gold"]
        self.other.test_input = ["trash province"]
        self.plr.play_card(self.bishop)
        self.assertEqual(self.plr.score["bishop"], 3)
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.assertTrue(self.other.piles[Piles.HAND].is_empty())
        self.assertEqual(self.g.trash_pile.size(), trash_size + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
