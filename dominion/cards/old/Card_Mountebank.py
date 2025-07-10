#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Mountebank(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+2 coin. Each other player may discard a Curse. If he doesn't, he gains a Curse and a Copper."
        self.name = "Mountebank"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            for card in plr.piles[Piles.HAND]:
                if card.name == "Curse":
                    player.output(f"Player {plr} discarded a curse")
                    plr.output(f"Discarded a Curse due to {player}'s Mountebank")
                    plr.discard_card(card)
                    break
            else:
                player.output(f"Player {plr} gained a curse and a copper")
                plr.output(f"Gained a Curse and Copper due to {player}'s Mountebank")
                try:
                    if curse := game.get_card_from_pile("Curse"):
                        plr.add_card(curse)
                except NoCardException:
                    plr.output("No more Curses")
                try:
                    if copper := game.get_card_from_pile("Copper"):
                        plr.add_card(copper)
                except NoCardException:
                    plr.output("No more Copper")


###############################################################################
class TestMountebank(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Mountebank"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.mountebank = self.g.get_card_from_pile("Mountebank")
        self.curse = self.g.get_card_from_pile("Curse")

    def test_hascurse(self) -> None:
        self.attacker.add_card(self.mountebank, Piles.HAND)
        self.victim.add_card(self.curse, Piles.HAND)
        self.attacker.play_card(self.mountebank)
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Curse")

    def test_nocurse(self) -> None:
        self.attacker.add_card(self.mountebank, Piles.HAND)
        self.attacker.play_card(self.mountebank)
        discards = [c.name for c in self.victim.piles[Piles.DISCARD]]
        self.assertEqual(sorted(discards), sorted(["Curse", "Copper"]))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
