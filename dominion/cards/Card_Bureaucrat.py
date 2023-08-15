#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


class Card_Bureaucrat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = """ Gain a Silver; put it on top of your deck. Each
            other player reveals a victory card from his hand and puts
            it on his deck (or reveals a hand with no victory cards)"""
        self.name = "Bureaucrat"
        self.cost = 4

    def special(self, game, player):
        player.gain_card("Silver", "topdeck")
        player.output("Added silver to deck")

        for pl in player.attack_victims():
            for card in pl.piles[Piles.HAND]:
                if card.isVictory():
                    pl.reveal_card(card)
                    pl.move_card(card, "topdeck")
                    pl.output(
                        f"Moved {card.name} to deck due to Bureaucrat played by {player.name}"
                    )
                    player.output(f"Player {pl.name} moved a {card.name} to the top")
                    break
            else:
                player.output(f"Player {pl.name} has no victory cards in hand")


###############################################################################
class TestBureaucrat(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Bureaucrat", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.bcard = self.g["Bureaucrat"].remove()
        self.plr.add_card(self.bcard, Piles.HAND)

    def test_hasvictory(self):
        self.victim.piles[Piles.HAND].set("Estate", "Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Silver")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.victim.piles[Piles.DECK][-1].name, "Estate")
        self.assertNotIn("Estate", self.victim.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")

    def test_novictory(self):
        self.victim.piles[Piles.HAND].set("Copper", "Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Province")
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.victim.piles[Piles.DECK][-1].name, "Province")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")

    def test_defense(self):
        self.victim.piles[Piles.DECK].set("Province")
        self.victim.piles[Piles.HAND].set("Estate", "Duchy", "Moat")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")
        self.assertEqual(self.victim.piles[Piles.DECK][-1].name, "Province")
        self.assertIn("Estate", self.victim.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
