#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Swamphag(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = "Until your next turn, when any other player buys a card, he gains a Curse. At the start of your next turn: +3 Coin"
        self.required_cards = ["Curse"]
        self.name = "Swamp Hag"
        self.cost = 5

    def special(self, game, player):
        pass

    def duration(self, game, player):
        player.add_coins(3)

    def hook_all_players_buy_card(self, game, player, owner, card):
        if player == owner:
            return
        player.gain_card("Curse")
        player.output("Gained a curse from %s's Swamp Hag" % owner.name)
        owner.output("Cursed %s when they bought a %s" % (player.name, card.name))


###############################################################################
class Test_Swamphag(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Swamp Hag"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.seahag = self.g["Swamp Hag"].remove()
        self.attacker.add_card(self.seahag, "hand")

    def test_play(self):
        self.attacker.play_card(self.seahag)
        self.attacker.end_turn()
        self.victim.buy_card(self.g["Copper"])
        self.assertEqual(self.attacker.durationpile[0].name, "Swamp Hag")
        self.assertIsNotNone(self.victim.in_discard("Curse"))
        self.attacker.start_turn()
        self.assertIsNotNone(self.attacker.in_played("Swamp Hag"))
        self.assertEqual(self.attacker.get_coins(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
