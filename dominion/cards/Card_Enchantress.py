#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, NoCardException


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

    def hook_all_players_pre_play(self, game, player, owner, card):
        if len(player.piles[Piles.PLAYED]) == 0:
            player.output(f"{owner.name}'s Enchantress gazump'd your {card.name}")
            player.add_actions(1)
            try:
                player.pickup_card()
            except NoCardException:
                pass
            return {"skip_card": True}
        return None


###############################################################################
class TestEnchantress(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, initcards=["Enchantress", "Remodel", "Moat"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Enchantress")
        self.r1 = self.g.get_card_from_pile("Remodel")
        self.m1 = self.g.get_card_from_pile("Moat")

    def test_play(self):
        """Play an Enchantress"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.vic.add_card(self.r1, Piles.HAND)
        self.vic.play_card(self.r1)
        self.assertEqual(self.vic.piles[Piles.HAND].size(), 5 + 1)  # Hand + Enchantress
        self.assertEqual(self.vic.actions.get(), 1)
        self.vic.add_card(self.m1, Piles.HAND)
        self.vic.play_card(self.m1)
        self.assertEqual(
            self.vic.piles[Piles.HAND].size(), 5 + 1 + 2
        )  # Hand + Enchantress + Moat
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
