#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Exorcist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night']
        self.base = 'nocturne'
        self.desc = "Trash a card from your hand. Gain a cheaper Spirit from one of the Spirit piles."
        self.name = 'Exorcist'
        self.cost = 4
        self.required_cards = [('Card', 'Ghost'), ('Card', 'Imp'), ('Card', "Will-o'-Wisp")]

    def special(self, game, player):
        trashed = player.plrTrashCard(prompt="Trash a card and gain a cheaper spirit")
        cost = trashed[0].cost
        options = []
        idx = 0
        for card in ('Ghost', 'Imp', "Will-o'-Wisp"):
            if game[card].cost < cost:
                sel = "{}".format(idx)
                toprint = "Get {}".format(card)
                options.append({'selector': sel, 'print': toprint, 'card': card})
                idx += 1
        if idx:
            o = player.userInput(options, "Gain a spirit")
            player.gainCard(o['card'])
        else:
            player.output("No spirits available at that price")


###############################################################################
class Test_Exorcist(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Exorcist'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Exorcist'].remove()

    def test_play(self):
        self.plr.setHand('Silver', 'Gold', 'Province')
        self.plr.test_input = ['Silver', 'Imp']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Imp'))
        self.assertIsNotNone(self.g.inTrash('Silver'))
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
