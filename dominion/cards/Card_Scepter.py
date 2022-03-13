#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Scepter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.RENAISSANCE
        self.desc = "When you play this, choose one: 2 coin; or replay an Action card you played this turn that's still in play."
        self.name = "Scepter"
        self.cost = 5

    def special(self, game, player):
        acts = [_ for _ in player.played if _.isAction()]
        if acts:
            get_coin = player.plrChooseOptions(
                "Pick one? ", ("2 Coin", True), ("Replay an action card", False)
            )
        else:
            get_coin = True
            player.output("No suitable cards - gaining coin")
        if get_coin:
            player.addCoin(2)
        else:
            card = player.cardSel(cardsrc=acts)
            player.add_card(card[0], "hand")
            player.played.remove(card[0])
            player.playCard(card[0], costAction=False)


###############################################################################
class Test_Scepter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Scepter", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Scepter"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_coin(self):
        self.plr.test_input = ["2 Coin"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_play_replay(self):
        self.plr.set_played("Moat")
        self.plr.test_input = ["Replay", "Moat"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
