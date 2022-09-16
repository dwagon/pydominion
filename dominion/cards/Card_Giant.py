#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Giant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """ Turn your Journey token over (it starts face up). If it's face
            down, +1 Coin. If it's face up, +5 Coin, and each other player
            reveals the top card of his deck, trashes it if it costs
            from 3 to 6, and otherwise discards it and gains a Curse """
        self.name = "Giant"
        self.required_cards = ["Curse"]
        self.cost = 5

    def special(self, game, player):
        if player.flip_journey_token():
            player.coins.add(5)
            for victim in player.attack_victims():
                c = victim.next_card()
                victim.reveal_card(c)
                if c.cost >= 3 and c.cost <= 6:
                    victim.trash_card(c)
                    victim.output("%s's Giant trashed your %s" % (player.name, c.name))
                    player.output("Trashed %s's %s" % (victim.name, c.name))
                else:
                    victim.output(
                        "%s's Giant discarded your %s and cursed you" % (player.name, c.name)
                    )
                    victim.add_card(c, "discard")
                    victim.gain_card("Curse")
        else:
            player.coins.add(1)


###############################################################################
class Test_Giant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Giant"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Giant"].remove()

    def test_play_journey_trashed(self):
        """Play a giant - good journey - trashable victim"""
        self.plr.hand.set()
        self.victim.deck.set("Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.journey_token = False
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertIn("Gold", self.g.trashpile)

    def test_play_journey_untrashed(self):
        """Play a giant - good journey - untrashable victim"""
        self.plr.hand.set()
        self.victim.deck.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.journey_token = False
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertNotIn("Copper", self.g.trashpile)
        self.assertIn("Curse", self.victim.discardpile)

    def test_play_no_journey(self):
        """Play a giant - bad journey"""
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.journey_token = True
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
