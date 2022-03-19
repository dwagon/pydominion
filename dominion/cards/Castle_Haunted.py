#!/usr/bin/env python

import unittest
from dominion import Game, Card
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_HauntedCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.TYPE_VICTORY, Card.TYPE_CASTLE]
        self.base = Game.EMPIRES
        self.cost = 6
        self.desc = """2VP. When you gain this during your turn, gain a Gold,
        and each other player with 5 or more cards in hand puts 2 cards from their hand onto their deck."""
        self.victory = 2
        self.name = "Haunted Castle"

    def hook_gain_this_card(self, game, player):
        player.gain_card("Gold")
        for plr in list(game.players.values()):
            if plr == player:
                continue
            if plr.hand.size() >= 5:
                cards = plr.card_sel(
                    num=2,
                    force=True,
                    prompt="%s's Haunted Castle: Select 2 cards to put onto your deck"
                    % player.name,
                )
                for card in cards:
                    plr.add_card(card, "topdeck")
                    plr.hand.remove(card)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class Test_HauntedCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Castles"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Haunted Castle":
                break

    def test_play(self):
        """Play a castle"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Haunted Castle"], 2)

    def test_gain(self):
        self.vic.set_hand("Copper", "Silver", "Gold", "Estate", "Province")
        self.vic.test_input = ["Silver", "Gold", "finish"]
        self.plr.gain_card(newcard=self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))
        self.assertIsNotNone(self.vic.in_deck("Silver"))
        self.assertIsNone(self.vic.in_hand("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
