#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Rabble(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+3 cards. Each other player reveals the top 3 cards of his
            deck, discards the revealed Actions and Treasures, and puts the rest
            back on top in any order he chooses."""
        self.name = "Rabble"
        self.cost = 5
        self.cards = 3

    def attack(self, victim: "Player.Player", attacker: "Player.Player") -> None:
        cards = []
        for _ in range(3):
            try:
                card = victim.next_card()
            except NoCardException:
                continue
            victim.reveal_card(card)
            if card.isAction() or card.isTreasure():
                victim.output(f"Discarding {card} due to {attacker.name}'s rabble")
                attacker.output(f"{victim.name} discarding {card}")
                victim.discard_card(card)
            else:
                cards.append(card)
        # TODO - let victim pick order
        for card in cards:
            victim.output(f"Putting {card} back on deck")
            attacker.output(f"{victim.name} keeping {card}")
            victim.add_card(card, Piles.DECK)

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Each other player reveals the top 3 cards of his deck,
        discard the revealed Actions and Treasures, and puts the
        rest back on top in any order he chooses"""
        for plr in player.attack_victims():
            self.attack(plr, player)


###############################################################################
class Test_Rabble(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Rabble", "Moat"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.rabble = self.g.get_card_from_pile("Rabble")
        self.moat = self.g.get_card_from_pile("Moat")
        self.attacker.add_card(self.rabble, Piles.HAND)

    def test_defended(self) -> None:
        self.victim.add_card(self.moat, Piles.HAND)
        self.attacker.play_card(self.rabble)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 6)  # 5 + moat
        self.assertEqual(self.attacker.piles[Piles.HAND].size(), 5 + 3)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())

    def test_no_defense(self) -> None:
        self.victim.piles[Piles.DECK].set("Copper", "Estate", "Rabble")
        self.attacker.play_card(self.rabble)
        self.assertEqual(self.victim.piles[Piles.DECK][-1].name, "Estate")
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.attacker.piles[Piles.HAND].size(), 5 + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
