#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Bureaucrat(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = """ Gain a Silver; put it on top of your deck. Each
            other player reveals a victory card from his hand and puts
            it on his deck (or reveals a hand with no victory cards)"""
        self.name = "Bureaucrat"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Silver", Piles.TOPDECK)
            player.output("Added silver to deck")
        except NoCardException:
            player.output("No more Silver")

        for victim in player.attack_victims():
            for card in victim.piles[Piles.HAND]:
                if card.isVictory():
                    victim.reveal_card(card)
                    victim.move_card(card, Piles.TOPDECK)
                    victim.output(f"Moved {card.name} to deck due to Bureaucrat played by {player}")
                    player.output(f"Player {victim} moved a {card} to the top")
                    break
            else:
                player.output(f"Player {victim} has no victory cards in hand")


###############################################################################
class TestBureaucrat(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Bureaucrat", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.bcard = self.g.get_card_from_pile("Bureaucrat")
        self.plr.add_card(self.bcard, Piles.HAND)

    def test_has_victory(self) -> None:
        self.victim.piles[Piles.HAND].set("Estate", "Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Silver")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.victim.piles[Piles.DECK][-1].name, "Estate")
        self.assertNotIn("Estate", self.victim.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")

    def test_no_victory(self) -> None:
        self.victim.piles[Piles.HAND].set("Copper", "Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Province")
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.victim.piles[Piles.DECK][-1].name, "Province")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")

    def test_defense(self) -> None:
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
