#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Banish """

import unittest
import Game
from Event import Event


###############################################################################
class Event_Banish(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Exile any number of cards with the same name from your hand."
        self.name = "Banish"
        self.cost = 4

    def special(self, game, player):
        cardnames = {_.name for _ in player.hand}
        options = [("Exile nothing", None)]
        for cname in cardnames:
            options.append(("Exile {} ({} in hand)".format(cname, player.hand.count(cname)), cname))
        card = player.plrChooseOptions(
            "Pick a card to exile",
            *options
        )
        if card is None:
            return
        if player.hand.count(card) == 1:
            player.exile_card(card)
            player.hand.remove(card)
        else:
            options = []
            for i in range(player.hand.count(card)+1):
                options.append(("Exile {} {}".format(i, card), i))
            count = player.plrChooseOptions(
                "How many to exile",
                *options)
            for _ in range(count):
                player.exile_card(card)
                player.hand.remove(card)


###############################################################################
class Test_Banish(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=['Banish'],
            initcards=['Cellar', 'Chapel', 'Moat', 'Militia', 'Village', 'Workshop'],
            badcards=['Hostelry', 'Border Village', 'Inn', 'Cursed Village']
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Banish']

    def test_Banish(self):
        """ Use Banish """
        self.plr.addCoin(5)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard('Horse'))
        self.assertEqual(self.plr.discardpile.size(), 5)

    def test_no_Banish(self):
        """ Use Banish with played lots """
        self.plr.setPlayed('Copper', 'Silver', 'Gold', 'Copper', 'Silver', 'Gold')
        self.plr.addCoin(5)
        self.plr.performEvent(self.card)
        self.assertIsNone(self.plr.in_discard('Horse'))
        self.assertEqual(self.plr.discardpile.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
