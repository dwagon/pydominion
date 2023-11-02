#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, NoCardException


###############################################################################
class Card_Swindler(Card.Card):
    """Swindler"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+2 Coin. Each other player trashed the top card of his deck and
            gains a card with the same cost that you choose."""
        self.name = "Swindler"
        self.cost = 3
        self.coin = 2

    def special(self, game, player):
        for victim in player.attack_victims():
            try:
                trashed_card = victim.pickup_card()
            except NoCardException:
                continue
            victim.trash_card(trashed_card)
            victim.output(f"{player.name}'s Swindler trashed your {trashed_card}")
            gained_card = player.plr_gain_card(
                trashed_card.cost,
                modifier="equal",
                recipient=victim,
                force=True,
                prompt=f"Pick which card {victim.name} will get",
            )
            if gained_card:
                victim.output(
                    f"{player.name} picked a {gained_card} to replace your trashed {trashed_card}"
                )


###############################################################################
class Test_Swindler(unittest.TestCase):
    """Test Swindler"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Swindler", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Swindler")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the Swindler"""
        self.victim.piles[Piles.HAND].set("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_defended(self):
        """Swindle a defended player"""
        tsize = self.g.trash_pile.size()
        self.victim.piles[Piles.HAND].set("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_attack(self):
        """Swindle an undefended player"""
        tsize = self.g.trash_pile.size()
        self.victim.piles[Piles.DECK].set("Gold")
        self.plr.test_input = ["Get Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
