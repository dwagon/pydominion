#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Taxman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'guilds'
        self.desc = """You may trash a Treasure from your hand.
        Each other player with 5 or more cards in hand discards a copy of it (or reveals a hand without it).
        Gain a Treasure card costing up to 3 more than the trashed card, putting it on top of your deck."""
        self.name = 'Taxman'
        self.cost = 4

    def special(self, game, player):
        treas = [c for c in player.hand if c.isTreasure()]
        cards = player.plrTrashCard(cardsrc=treas, prompt='Pick card to trash. Others discard that. You gain a treasure costing 3 more')
        if not cards:
            return
        card = cards[0]
        for vic in player.attackVictims():
            if vic.handSize() >= 5:
                viccard = vic.inHand(card.name)
                if viccard:
                    vic.output("Discarding %s due to %s's Taxman" % (viccard.name, player.name))
                    player.output("%s discarded a %s" % (vic.name, viccard.name))
                    vic.discardCard(viccard)
                else:
                    player.output("%s doesn't have a %s" % (vic.name, card.name))
                    for c in vic.hand:
                        vic.revealCard(c)
        cardcost = player.cardCost(card) + 3
        player.plrGainCard(cost=cardcost, types={'treasure': True})


###############################################################################
class Test_Taxman(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Taxman'], badcards=["Fool's Gold"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Taxman'].remove()

    def test_play(self):
        """ Play a Taxman """
        self.plr.setHand('Silver')
        self.victim.setHand('Copper', 'Copper', 'Estate', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Silver', 'Get Gold']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.victim.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
