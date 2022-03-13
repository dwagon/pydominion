#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Giant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.ADVENTURE
        self.desc = """ Turn your Journey token over (it starts face up). If it's face
            down, +1 Coin. If it's face up, +5 Coin, and each other player
            reveals the top card of his deck, trashes it if it costs
            from 3 to 6, and otherwise discards it and gains a Curse """
        self.name = "Giant"
        self.required_cards = ["Curse"]
        self.cost = 5

    def special(self, game, player):
        if player.flip_journey_token():
            player.addCoin(5)
            for victim in player.attackVictims():
                c = victim.nextCard()
                victim.reveal_card(c)
                if c.cost >= 3 and c.cost <= 6:
                    victim.trash_card(c)
                    victim.output("%s's Giant trashed your %s" % (player.name, c.name))
                    player.output("Trashed %s's %s" % (victim.name, c.name))
                else:
                    victim.output(
                        "%s's Giant discarded your %s and cursed you"
                        % (player.name, c.name)
                    )
                    victim.addCard(c, "discard")
                    victim.gainCard("Curse")
        else:
            player.addCoin(1)


###############################################################################
class Test_Giant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Giant"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Giant"].remove()

    def test_play_journey_trashed(self):
        """Play a giant - good journey - trashable victim"""
        self.plr.setHand()
        self.victim.setDeck("Gold")
        self.plr.addCard(self.card, "hand")
        self.plr.journey_token = False
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)
        self.assertIsNotNone(self.g.in_trash("Gold"))

    def test_play_journey_untrashed(self):
        """Play a giant - good journey - untrashable victim"""
        self.plr.setHand()
        self.victim.setDeck("Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.journey_token = False
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)
        self.assertIsNone(self.g.in_trash("Copper"))
        self.assertIsNotNone(self.victim.in_discard("Curse"))

    def test_play_no_journey(self):
        """Play a giant - bad journey"""
        self.plr.setHand()
        self.plr.addCard(self.card, "hand")
        self.plr.journey_token = True
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
