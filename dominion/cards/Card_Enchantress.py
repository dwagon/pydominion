#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Enchantress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """Until your next turn, the first time each other player plays an
            Action card on their turn, they get +1 Card and +1 Action instead of
            following its instructions. At the start of your next turn, +2 Cards"""
        self.name = "Enchantress"
        self.cost = 3

    def duration(self, game, player):
        player.pickup_cards(2)

    def hook_all_players_pre_action(self, game, player, owner, card):
        if len(player.played) == 0:
            player.output(f"{owner.name}'s Enchantress gazump'd your {card.name}")
            player.add_actions(1)
            player.pickup_card()
            return {"skip_card": True}
        return None


###############################################################################
class TestEnchantress(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Enchantress", "Remodel", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Enchantress"].remove()
        self.r1 = self.g["Remodel"].remove()
        self.m1 = self.g["Moat"].remove()

    def test_play(self):
        """Play an Enchantress"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.vic.add_card(self.r1, "hand")
        self.vic.play_card(self.r1)
        self.assertEqual(self.vic.hand.size(), 5 + 1)  # Hand + Enchantress
        self.assertEqual(self.vic.actions.get(), 1)
        self.vic.add_card(self.m1, "hand")
        self.vic.play_card(self.m1)
        self.assertEqual(self.vic.hand.size(), 5 + 1 + 2)  # Hand + Enchantress + Moat
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
