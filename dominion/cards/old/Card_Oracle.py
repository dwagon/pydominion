#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Oracle(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.HINTERLANDS
        self.desc = """Each player (including you) reveals the top 2 cards of his deck, and you choose one:
        either he discards them or he puts them back on top in an order he chooses.  +2 cards """
        self.name = "Oracle"
        self.cost = 3

    def special(self, game, player):
        for plr in player.attack_victims():
            self.attack(player, plr, "%s's" % plr.name)
        self.attack(player, player, "your")
        player.pickup_cards(2)

    def attack(self, player, victim, name):
        cards = []
        for _ in range(2):
            card = victim.next_card()
            victim.reveal_card(card)
            cards.append(card)
        cardnames = ", ".join([c.name for c in cards])
        discard = player.plr_choose_options(
            "What to do with %s cards: %s" % (name, cardnames),
            ("Discard %s" % cardnames, True),
            ("Put %s on top of deck" % cardnames, False),
        )
        if discard:
            for card in cards:
                victim.discard_card(card)
            victim.output("%s's Oracle discarded your %s" % (player.name, cardnames))
        else:
            for card in cards:
                victim.add_card(card, "topdeck")
            victim.output("%s's Oracle put %s on top of your deck" % (player.name, cardnames))


###############################################################################
class Test_Oracle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Oracle"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Oracle"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_card(self):
        """Play Oracle"""
        self.vic.deck.set("Estate", "Duchy", "Province")
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.test_input = ["discard", "top"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.discardpile)
        self.assertIn("Province", self.vic.discardpile)
        self.assertIn("Silver", self.plr.hand)
        self.assertIn("Gold", self.plr.hand)
        self.assertEqual(self.plr.hand.size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
