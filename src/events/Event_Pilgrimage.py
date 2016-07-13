#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Pilgrimage(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = """Once per turn: Turn your Journey token over; then if it's face up,
        choose up to 3 differently named cards you have in play and gain a copy of each."""
        self.name = "Pilgrimage"
        self.cost = 4

    def special(self, game, player):
        if not player.do_once('Pilgrimage'):
            player.output("Already performed a Pilgrimage this turn")
            return
        if not player.flip_journey_token():
            player.output("Flipped Journey token to face down")
            return
        cardnames = set([c.name for c in player.played if c.purchasable])
        selected = []
        while True:
            options = [{'selector': '0', 'print': 'Finish', 'opt': None}]
            index = 1
            for cn in cardnames:
                options.append({'selector': '%d' % index, 'print': cn, 'opt': cn})
                index += 1
            choice = player.userInput(options, "Select a card to gain - up to 3!")
            if choice['opt']:
                selected.append(choice['opt'])
                cardnames.remove(choice['opt'])
            else:
                break
            if len(selected) == 3:
                break
        for card in selected:
            player.gainCard(card)
            player.output("Gained a %s" % card.name)


###############################################################################
class Test_Pilgrimage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Pilgrimage'], initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Pilgrimage']

    def test_play(self):
        """ Perform a Pilgrimage """
        self.plr.setPlayed('Moat', 'Silver', 'Gold', 'Copper', 'Duchy')
        self.plr.test_input = ['moat', 'silver', 'finish']
        self.plr.journey_token = False
        self.plr.addCoin(4)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Moat'))
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertTrue(self.plr.journey_token)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
