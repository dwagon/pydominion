#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Apothecary"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Apothecary(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = """+1 Card; +1 Action; Reveal the top 4 cards of your deck.
            Put the Coppers and Potions into your hand.
            Put the rest back in any order."""
        self.name = "Apothecary"
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.potcost = True
        self.required_cards = ["Potion"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal the top 4 cards of your deck. Put the revealed
        Coppers and Potions into your hand. Put the other cards
        back on top of your deck in any order"""
        unput = []
        for _ in range(4):
            try:
                card = player.next_card()
            except NoCardException:
                continue
            player.reveal_card(card)
            if card.name in ("Copper", "Potion"):
                player.output(f"Putting {card} in hand")
                player.add_card(card, Piles.HAND)
            else:
                unput.append(card)
        for card in unput:
            player.output(f"Putting {card} back in deck")
            player.add_card(card, "deck")


###############################################################################
class TestApothecary(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Apothecary"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_none(self) -> None:
        self.plr.piles[Piles.HAND].set("Apothecary")
        apoth = self.plr.piles[Piles.HAND][0]
        self.plr.piles[Piles.DECK].set("Duchy", "Estate", "Estate", "Estate", "Province")
        self.plr.play_card(apoth)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)  # P
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 4)  # D + E + E + E

    def test_some(self) -> None:
        self.plr.piles[Piles.HAND].set("Apothecary")
        apoth = self.plr.piles[Piles.HAND][0]
        self.plr.piles[Piles.DECK].set("Duchy", "Potion", "Copper", "Estate", "Province")
        self.plr.play_card(apoth)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)  # P + C + Pot
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 2)  # E + D


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
