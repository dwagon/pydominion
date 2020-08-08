#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_PirateShip(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = Game.SEASIDE
        self.desc = """Choose one: Each other player reveals the top 2 cards of his deck,
        trashes a revealed Treasure that you choose, discards the rest,
        and if anyone trashed a Treasure you take a Coin token;
        or, +1 per Coin token you've taken with Pirate Ships this game."""
        self.name = 'Pirate Ship'
        self.cost = 4

    def special(self, game, player):
        choice = player.plrChooseOptions(
            "Pick one",
            ("Each other player reveals the top 2 cards of his deck, trashes a " +
             "revealed Treasure that you choose, discards the rest, and if anyone " +
             "trashed a Treasure you take a Coin token", 'attack'),
            ("+%d = +1 per treasure you've taken with Pirate Ships this game." % player._pirate_ship, 'spend')
        )
        if choice == 'attack':
            trashed = False
            for victim in player.attackVictims():
                if self.attack_player(player, victim):
                    trashed = True
            if trashed:
                player._pirate_ship += 1
        else:
            player.addCoin(player._pirate_ship)

    def attack_player(self, player, victim):
        trashed = False
        cards = []
        for _ in range(2):
            card = victim.nextCard()
            victim.revealCard(card)
            if card.isTreasure():
                cards.append(card)
            else:
                victim.output("%s's Pirate Ship discarded your %s" % (player.name, card.name))
                victim.addCard(card, 'discard')
        if cards:
            to_trash = player.plrTrashCard(
                prompt="Trash a card from %s" % victim.name,
                cardsrc=cards)
            if to_trash:
                trashed = True
                for card in cards:
                    if card not in to_trash:
                        victim.addCard(card, 'discard')
                        victim.output("Discarded %s" % card.name)
                    else:
                        victim.output("Trashed %s" % card.name)
        else:
            player.output("Player %s has no treasures to trash" % victim.name)
        return trashed

    def hook_gain_this_card(self, game, player):
        if not hasattr(player, '_pirate_ship'):
            player._pirate_ship = 0
        return {}


###############################################################################
class Test_PirateShip(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Pirate Ship'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Pirate Ship'].remove()
        self.plr.gainCard(newcard=self.card, destination='hand')

    def test_play_attack(self):
        tsize = self.g.trashSize()
        self.vic.setDeck('Copper', 'Estate')
        self.plr.test_input = ['Each other', 'copper']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.g.trashSize(), tsize + 1)
            self.assertIsNotNone(self.g.in_trash('Copper'))
            self.assertEqual(self.plr._pirate_ship, 1)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_spend(self):
        self.plr._pirate_ship = 2
        self.plr.test_input = ['per treasure']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
