#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Enchantress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_DURATION]
        self.base = Game.EMPIRES
        self.desc = """Until your next turn, the first time each other player plays an
            Action card on their turn, they get +1 Card and +1 Action instead of
            following its instructions. At the start of your next turn, +2 Cards"""
        self.name = "Enchantress"
        self.cost = 3

    def duration(self, game, player):
        player.add_cards(2)

    def hook_allPlayers_preAction(self, game, player, owner, card):
        if len(player.played) == 0:
            player.output(
                "{}'s Enchantress gazump'd your {}".format(owner.name, card.name)
            )
            player.addActions(1)
            player.pickup_card()
            return {"skip_card": True}
        return None


###############################################################################
class Test_Enchantress(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=2, initcards=["Enchantress", "Remodel", "Moat"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Enchantress"].remove()
        self.r1 = self.g["Remodel"].remove()
        self.m1 = self.g["Moat"].remove()

    def test_play(self):
        """Play an Enchantress"""
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.vic.add_card(self.r1, "hand")
        self.vic.playCard(self.r1)
        self.assertEqual(self.vic.hand.size(), 5 + 1)  # Hand + Ench
        self.assertEqual(self.vic.get_actions(), 1)
        self.vic.add_card(self.m1, "hand")
        self.vic.playCard(self.m1)
        self.g.print_state()
        self.assertEqual(self.vic.hand.size(), 5 + 1 + 2)  # Hand + Ench + Moat


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
