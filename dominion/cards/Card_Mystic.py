#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Mystic(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 coin, +1 action; Name a card. Reveal the top card of your deck. 
        If it's the named card, put it into your hand."""
        self.name = "Mystic"
        self.actions = 1
        self.coin = 2
        self.cost = 5

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Name a card. Reveal the top card of your deck. If it's
        the named card, put it into your hand"""
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for name, card_pile in sorted(game.get_card_piles()):
            options.append(
                {"selector": f"{index}", "print": f"Guess {name}", "card": name}
            )
            index += 1
        o = player.user_input(options, "Guess the top card")
        if not o["card"]:
            return
        card = player.next_card()
        player.reveal_card(card)
        if o["card"] == card.name:
            player.output("You guessed correctly")
            player.add_card(card, Piles.HAND)
        else:
            player.output(f"You chose poorly - it was a {card}")
            player.add_card(card, "topdeck")


###############################################################################
class TestMystic(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Mystic"],
            badcards=["Tournament", "Fool's Gold", "Pooka"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mystic")

    def test_play(self) -> None:
        """No guess should still get results"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_good(self) -> None:
        """When the guess is good the card should move to the hand"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertTrue(self.plr.piles[Piles.DECK].is_empty())

    def test_bad(self) -> None:
        """When the guess is bad the card should stay on the deck"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Province")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
