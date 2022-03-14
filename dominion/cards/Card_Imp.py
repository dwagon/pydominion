#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Imp(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_SPIRIT]
        self.base = Game.NOCTURNE
        self.desc = "+2 Cards; You may play an Action card from your hand that you don't have a copy of in play."
        self.name = "Imp"
        self.purchasable = False
        self.insupply = False
        self.cards = 2
        self.cost = 2
        self.numcards = 13

    def special(self, game, player):
        # Get action cards in hand
        ac = [_ for _ in player.hand if _.isAction()]
        if not ac:
            player.output("No action cards")
            return
        # Select ones that haven't been played
        sac = [_ for _ in ac if not player.in_played(_.name)]
        if not sac:
            player.output("No unplayed action cards")
            return
        options = [{"selector": "0", "print": "Nothing", "card": None}]
        index = 1
        for p in sac:
            selector = "{}".format(index)
            toprint = "Play {} ({})".format(p.name, p.description(player))
            options.append({"selector": selector, "print": toprint, "card": p})
            index += 1
        o = player.user_input(options, "What card do you want to play?")
        if o["card"]:
            player.play_card(o["card"], costAction=False)


###############################################################################
class Test_Imp(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Imp", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Imp"].remove()

    def test_played(self):
        self.plr.set_hand("Moat", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.set_played("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2 + 2)

    def test_not_played(self):
        self.plr.set_hand("Moat", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(
            self.plr.hand.size(), 2 + 2 + 1
        )  # 2 for moat, 2 for imp, 1 for hand


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
