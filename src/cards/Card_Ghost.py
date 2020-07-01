#!/usr/bin/env python

import unittest
import Game
from Card import Card
from PlayArea import PlayArea


###############################################################################
class Card_Ghost(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration', 'spirit']
        self.base = 'nocturne'
        self.desc = """Reveal cards from your deck until you reveal an Action.
            Discard the other cards and set aside the Action. At the start of
            your next turn, play it twice."""
        self.name = 'Ghost'
        self.purchasable = False
        self.insupply = False
        self.cost = 4

    def night(self, game, player):
        if not hasattr(player, '_ghost_reserve'):
            player._ghost_reserve = PlayArea([])
        count = len(player.allCards())
        while count:
            card = player.nextCard()
            player.revealCard(card)
            if card.isAction():
                player._ghost_reserve.add(card)
                break
            player.addCard(card, 'discard')
            count -= 1
        else:
            player.output("No action cards in deck")
            return

    def duration(self, game, player):
        if not hasattr(player, '_ghost_reserve'):
            return
        for card in player._ghost_reserve[:]:
            player.output("Ghost playing {}".format(card.name))
            for _ in range(2):
                player.playCard(card, discard=False, costAction=False)
            player._ghost_reserve.remove(card)


###############################################################################
class Test_Ghost(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Ghost', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Ghost'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_with_no_actions(self):
        """ Play a Ghost with no actions """
        self.plr.phase = 'night'
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr._ghost_reserve), 0)

    def test_duration(self):
        try:
            self.plr.setDeck('Silver', 'Gold', 'Estate', 'Silver', 'Moat', 'Copper')
            self.plr.setDiscard('Silver', 'Gold', 'Estate', 'Silver', 'Moat', 'Copper')
            self.plr.phase = 'night'
            self.plr.playCard(self.card)
            self.plr.endTurn()
            self.plr.startTurn()
            self.assertEqual(self.plr.handSize(), 5 + 2 * 2)    # Hand + Moat *2
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
