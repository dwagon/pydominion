#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Conclave(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+2 Coin; You may play an Action card from your hand that you don't have a copy of in play. If you do, +1 Action."
        self.name = "Conclave"
        self.cost = 4
        self.coin = 2

    def special(self, game, player):
        ac = [_ for _ in player.hand if _.isAction()]
        if not ac:
            player.output("No actions to play")
            return
        sac = [_ for _ in ac if _.name not in player.played]
        if not sac:
            player.output("No suitable actions to play")
            return
        options = [{"selector": "0", "print": "Nothing", "card": None}]
        index = 1
        for p in sac:
            selector = f"{index}"
            toprint = f"Play {p.name}"
            options.append({"selector": selector, "print": toprint, "card": p})
            index += 1
        o = player.user_input(options, "What card do you want to play?")
        if o["card"]:
            player.play_card(o["card"], costAction=False)
            player.add_actions(1)


###############################################################################
class Test_Conclave(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Conclave", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Conclave"].remove()

    def test_played(self):
        self.plr.hand.set("Moat", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.played.set("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_not_played(self):
        self.plr.hand.set("Moat", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
