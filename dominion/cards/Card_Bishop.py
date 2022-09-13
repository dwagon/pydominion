#!/usr/bin/env python

import unittest
from dominion import Card, Game


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

    @classmethod
    def trashOwnCard(cls, game, player):
        tc = player.plr_trash_card(
            printcost=True, prompt="Gain VP worth half the cost of the card you trash"
        )
        if not tc:
            return
        card = tc[0]
        points = int(card.cost / 2)
        player.add_score("bishop", points)
        player.output(f"Trashing {card.name} for {points} points")

    @classmethod
    def trashOtherCard(cls, game, player, victim):
        victim.output(f"{player.name}'s bishop lets you trash a card")
        tc = victim.plr_trash_card()
        if tc:
            victim.output(f"Trashing {tc[0].name}")
        else:
            victim.output("All mine I tell you, all mine")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Trash an estate, then a copper else nothing
    es = player.hand["estate"]
    if es:
        return [es]
    cu = player.hand["copper"]
    if cu:
        return [cu]
    return []


###############################################################################
class Test_Bishop(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Bishop"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.bishop = self.g["Bishop"].remove()

    def test_play(self):
        self.plr.add_card(self.bishop, "hand")
        self.plr.test_input = ["finish"]
        self.other.test_input = ["finish"]
        self.plr.play_card(self.bishop)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_trash(self):
        self.plr.hand.set("Gold")
        self.plr.add_card(self.bishop, "hand")
        self.plr.test_input = ["trash gold"]
        self.other.test_input = ["finish"]
        self.plr.play_card(self.bishop)
        self.assertEqual(self.plr.score["bishop"], 3)
        self.assertTrue(self.plr.hand.is_empty())
        self.assertIn("Gold", self.g.trashpile)

    def test_bothtrash(self):
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Gold")
        self.other.hand.set("Province")
        self.plr.add_card(self.bishop, "hand")
        self.plr.test_input = ["trash gold"]
        self.other.test_input = ["trash province"]
        self.plr.play_card(self.bishop)
        self.assertEqual(self.plr.score["bishop"], 3)
        self.assertTrue(self.plr.hand.is_empty())
        self.assertTrue(self.other.hand.is_empty())
        self.assertEqual(self.g.trashpile.size(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
