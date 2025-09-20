#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Aristocrat"""

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Aristocrat(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """If the number of Aristocrats you have in play is: 1 or 5: +3 Actions;
            2 or 6: +3 Cards; 3 or 7: +$3; 4 or 8: +3 Buys."""
        self.name = "Aristocrat"
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player"):
        count = 0
        for card in player.piles[Piles.PLAYED]:
            if card.name == "Aristocrat":
                count += 1
        player.output(f"{count} Aristocrats in play")
        if count in (1, 5):
            player.output("Gaining 3 actions")
            player.actions.add(3)
        elif count in (2, 6):
            player.output("Picking up 3 cards")
            player.pickup_cards(3)
        elif count in (3, 7):
            player.output("Gaining 3 coins")
            player.coins.add(3)
        elif count in (4, 8):
            player.output("Gaining 3 buys")
            player.buys.add(3)


###############################################################################
class Test_Aristocrat(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Aristocrat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Aristocrat")

    def test_play_1(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 3 - 1)  # Actions go up
        self.assertEqual(self.plr.coins.get(), coins)
        self.assertEqual(self.plr.buys.get(), buys)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size - 1)

    def test_play_2(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Aristocrat")
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions - 1)
        self.assertEqual(self.plr.coins.get(), coins)
        self.assertEqual(self.plr.buys.get(), buys)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 3 - 1)  # Cards go up

    def test_play_3(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Aristocrat", "Aristocrat")
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions - 1)
        self.assertEqual(self.plr.coins.get(), coins + 3)  # Coins go up
        self.assertEqual(self.plr.buys.get(), buys)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size - 1)

    def test_play_4(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Aristocrat", "Aristocrat", "Aristocrat")
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions - 1)
        self.assertEqual(self.plr.coins.get(), coins)
        self.assertEqual(self.plr.buys.get(), buys + 3)  # Buys go up
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
