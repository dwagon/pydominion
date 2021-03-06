#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Raider(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT, Card.TYPE_DURATION, Card.TYPE_ATTACK]
        self.base = Game.NOCTURNE
        self.desc = """Each other player with 5 or more cards in hand discards
            a copy of a card you have in play (or reveals they can't). At the
            start of your next turn, +3 Coins"""
        self.name = 'Raider'
        self.cost = 6

    def duration(self, game, player):
        player.addCoin(3)

    def night(self, game, player):
        inplay = {_.name for _ in player.played}
        for pl in player.attackVictims():
            if pl.hand.size() >= 5:
                player.output("Raiding {}".format(pl.name))
                todiscard = []
                for c in pl.hand:
                    if c.name in inplay:
                        pl.output("{}'s Raider discarded your {}".format(player.name, c.name))
                        player.output("Raider discarded {}'s {}".format(pl.name, c.name))
                        todiscard.append(c)
                if not todiscard:
                    for card in pl.hand:
                        pl.revealCard(card)
                for c in todiscard[:]:
                    pl.discardCard(c)


###############################################################################
class Test_Raider(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Raider'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Raider'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Raider """
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.setPlayed('Gold', 'Silver')
        self.vic.setHand('Silver', 'Gold', 'Estate', 'Copper', 'Copper')
        self.plr.playCard(self.card)
        try:
            self.assertIsNotNone(self.vic.in_discard('Gold'))
            self.assertIsNotNone(self.vic.in_discard('Silver'))
            self.assertIsNone(self.vic.in_hand('Gold'))
            self.assertIsNone(self.vic.in_hand('Silver'))
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise
        self.plr.end_turn()
        self.plr.start_turn()
        try:
            self.assertEqual(self.plr.getCoin(), 3)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
