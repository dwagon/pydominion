#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Sorcerer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_WIZARD, Card.TYPE_ATTACK]
        self.base = Game.ALLIES
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.name = "Sorcerer"
        self.desc = """+1 Card; +1 Action; Each other player names a card,
            then reveals the top card of their deck. If wrong, they gain a Curse."""

    def special(self, game, player):
        for plr in player.attack_victims():
            cps = [_ for _ in game.cardpiles if game.cardpiles[_].purchasable]
            options = []
            for cp in cps:
                options.append((cp, cp))
            pick = plr.plr_choose_options(
                "Sorcerer: Guess the top card correctly or get a curse", *options
            )
            tpcrd = plr.deck.top_card()
            player.reveal_card(tpcrd)
            if tpcrd.name != pick:
                player.output(f"Top card is {tpcrd.name} not {pick}")
                plr.gain_card("Curse")
            else:
                player.output(f"Guessed {pick} correctly")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """ Possibly not the best guess, but might be good enough """
    return "Copper"


###############################################################################
class Test_Sorcerer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Wizards"], use_liaisons=True)
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play_hit(self):
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Sorcerer":
                break
        self.plr.add_card(card, "hand")
        hndsz = self.plr.hand.size()
        self.vic.set_deck("Duchy")
        self.vic.test_input = ["Duchy"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.hand.size(), hndsz)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNone(self.vic.in_discard("Curse"))

    def test_play_miss(self):
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Sorcerer":
                break
        self.plr.add_card(card, "hand")
        hndsz = self.plr.hand.size()
        self.vic.set_deck("Duchy")
        self.vic.test_input = ["Estate"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.hand.size(), hndsz)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.vic.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
