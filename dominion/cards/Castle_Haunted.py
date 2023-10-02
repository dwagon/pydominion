#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Haunted_Castle """

import unittest
from dominion import Game, Card, Piles
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_HauntedCastle(CastleCard):
    """Haunted Castle"""

    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.CASTLE]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 6
        self.desc = """2VP. When you gain this during your turn, gain a Gold,
            and each other player with 5 or more cards in hand puts 2 cards from
            their hand onto their deck."""
        self.victory = 2
        self.name = "Haunted Castle"
        self.pile = "Castles"

    def hook_gain_this_card(self, game, player):
        player.gain_card("Gold")
        for plr in list(game.players.values()):
            if plr == player:
                continue
            if plr.piles[Piles.HAND].size() >= 5:
                cards = plr.card_sel(
                    num=2,
                    force=True,
                    prompt=f"{player.name}'s Haunted Castle: Select 2 cards to put onto your deck",
                )
                for card in cards:
                    plr.move_card(card, "topdeck")


###############################################################################
def botresponse(
    player, kind, args=None, kwargs=None
):  # pragma: no cover pylint: disable=unused-argument
    """Bot Response"""
    return player.pick_to_discard(2)


###############################################################################
class Test_HauntedCastle(unittest.TestCase):
    """Test Haunted Castle"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Castles"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Castles", "Haunted Castle")

    def test_play(self):
        """Play a castle"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Haunted Castle"], 2)

    def test_gain(self):
        """Test gaining this card"""
        self.vic.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Province")
        self.vic.test_input = ["Silver", "Gold", "finish"]
        self.plr.gain_card(new_card=self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.vic.piles[Piles.DECK])
        self.assertNotIn("Silver", self.vic.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
