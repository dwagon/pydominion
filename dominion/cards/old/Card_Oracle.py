#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Oracle(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
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
            victim.output(
                "%s's Oracle put %s on top of your deck" % (player.name, cardnames)
            )


###############################################################################
class TestOracle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Oracle"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Oracle"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play Oracle"""
        self.vic.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.test_input = ["discard", "top"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.piles[Piles.DISCARD])
        self.assertIn("Province", self.vic.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
