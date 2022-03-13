#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bishop(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
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
                self.trashOwnCard(game, player)
            else:
                self.trashOtherCard(game, player, plr)

    def trashOwnCard(self, game, player):
        tc = player.plrTrashCard(
            printcost=True, prompt="Gain VP worth half the cost of the card you trash"
        )
        if not tc:
            return
        card = tc[0]
        points = int(card.cost / 2)
        player.addScore("bishop", points)
        player.output("Trashing %s for %d points" % (card.name, points))

    def trashOtherCard(self, game, player, victim):
        victim.output("%s's bishop lets you trash a card" % player.name)
        tc = victim.plrTrashCard()
        if tc:
            victim.output("Trashing %s" % tc[0].name)
        else:
            victim.output("All mine I tell you, all mine")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Trash an estate, then a copper else nothing
    es = player.in_hand("estate")
    if es:
        return [es]
    cu = player.in_hand("copper")
    if cu:
        return [cu]
    return []


###############################################################################
class Test_Bishop(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Bishop"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.bishop = self.g["Bishop"].remove()

    def test_play(self):
        self.plr.add_card(self.bishop, "hand")
        self.plr.test_input = ["finish"]
        self.other.test_input = ["finish"]
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_trash(self):
        self.plr.set_hand("Gold")
        self.plr.add_card(self.bishop, "hand")
        self.plr.test_input = ["trash gold"]
        self.other.test_input = ["finish"]
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.score["bishop"], 3)
        self.assertTrue(self.plr.hand.is_empty())
        self.assertIsNotNone(self.g.in_trash("Gold"))

    def test_bothtrash(self):
        tsize = self.g.trashSize()
        self.plr.set_hand("Gold")
        self.other.set_hand("Province")
        self.plr.add_card(self.bishop, "hand")
        self.plr.test_input = ["trash gold"]
        self.other.test_input = ["trash province"]
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.score["bishop"], 3)
        self.assertTrue(self.plr.hand.is_empty())
        self.assertTrue(self.other.hand.is_empty())
        self.assertEqual(self.g.trashSize(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
