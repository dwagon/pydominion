#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Fortune_Hunter"""
import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_FortuneHunter(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+$2; Look at the top 3 cards of your deck. You may play a Treasure from them. 
        Put the rest back in any order."""
        self.name = "Fortune Hunter"
        self.cost = 4
        self.coin = 2

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Look at the top 3 cards of your deck. You may play a Treasure from them."""
        pickup_cards = []
        for _ in range(3):
            card = player.next_card()
            if card is not None:
                pickup_cards.append(card)
        treasures = [_ for _ in pickup_cards if _.isTreasure()]
        to_play = None
        if treasures:
            options = [("Play nothing", None)]
            for treasure in treasures:
                options.append((f"Play {treasure}", treasure))
            to_play = player.plr_choose_options("Pick a treasure to play", *options)
            if to_play:
                player.add_card(to_play, Piles.HAND)
                player.play_card(to_play, cost_action=False)
        else:
            player.output("No treasure cards")
        for card in pickup_cards:
            if card != to_play:
                player.add_card(card, Piles.DECK)


###############################################################################
class Test_FortuneHunter(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Fortune Hunter"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fortune Hunter")

    def test_play(self) -> None:
        """Play Fortune Hunter"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2 + 3)  # 2 for card, 3 for gold
        self.assertIn("Estate", self.plr.piles[Piles.DECK])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])

    def test_play_none(self) -> None:
        """Play FH and select none"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Nothing"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)  # 2 for card
        self.assertIn("Estate", self.plr.piles[Piles.DECK])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
