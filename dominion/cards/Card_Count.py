#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Count"""
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Count(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Choose one: Discard 2 cards; or put a card from your hand
            on top of your deck; or gain a Copper. Choose one: +3 Coin; or trash
            your hand; or gain a Duchy"""
        self.name = "Count"
        self.cost = 5

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Choose one: Discard 2 cards; or put a card from your
        hand on top of your deck; or gain a copper.

        Choose one: +3 coin, or trash your hand or gain a Duchy"""

        ans = player.plr_choose_options(
            "What do you want to do?",
            ("Discard 2 cards", "discard"),
            ("Put a card from you hand on top of your deck", "put_card"),
            ("Gain a copper", "copper"),
        )
        if ans == "copper":
            try:
                player.gain_card("Copper")
                player.output("Gained a copper")
            except NoCardException:
                player.output("No more Copper")
        elif ans == "put_card":
            self.put_card(player)
        else:
            player.plr_discard_cards(2)

        ans = player.plr_choose_options(
            "What do you want to do now?",
            ("+3 coin", "coin"),
            ("Trash hand", "trash"),
            ("Gain Duchy", "duchy"),
        )
        if ans == "duchy":
            try:
                player.gain_card("Duchy")
                player.output("Gained a duchy")
            except NoCardException:
                player.output("No more Duchys")
        elif ans == "trash":
            for card in player.piles[Piles.HAND]:
                player.output(f"Trashing {card}")
                player.trash_card(card)
        else:
            player.coins.add(3)

    ###########################################################################
    def put_card(self, player: Player.Player) -> None:
        """Put a card from your hand on top of your deck"""
        index = 1
        options = []
        for card in player.piles[Piles.HAND]:
            pr = f"Put {card} on top of your deck"
            options.append({"selector": f"{index}", "print": pr, "card": card})
            index += 1
        if not options:
            return
        o = player.user_input(options, "Select card to put on top of your deck")
        player.output(f"Moving {o['card']} to top of deck")
        player.move_card(o["card"], Piles.TOPDECK)


###############################################################################
class TestCount(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Count"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Count")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Silver", "Province", "Gold")

    def test_discard(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        # Discard, select card 1 and card 2, finish selecting, +3 coin
        self.plr.test_input = [
            "discard 2",
            "discard estate",
            "discard copper",
            "finish",
            "+3 coin",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)

    def test_top_deck(self) -> None:
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        # top deck, card select, +3 coin
        self.plr.test_input = ["top of your deck", "put gold", "+3 coin"]
        self.plr.play_card(self.card)
        nc = self.plr.next_card()
        self.assertEqual(nc.name, "Gold")

    def test_gain_copper(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["gain a copper", "+3 coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Copper")

    def test_gain_gold(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["gain a copper", "+3 coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)

    def test_trash_hand(self) -> None:
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["gain a copper", "trash hand"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.assertEqual(self.g.trash_pile.size(), tsize + 5)

    def test_gain_duchy(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["gain a copper", "gain duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
