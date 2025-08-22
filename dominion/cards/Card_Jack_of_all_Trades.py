#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, NoCardException, Player


###############################################################################
class Card_Jack_of_all_Trades(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Gain a Silver.
            Look at the top card of your deck; discard it or put it back.
            Draw until you have 5 cards in your hand.
            You may trash a card from your hand that is not a Treasure."""
        self.name = "Jack of all Trades"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Silver")
        except NoCardException:
            player.output("No more Silver")

        try:
            card = player.next_card()
        except NoCardException:
            pass
        else:
            if player.plr_choose_options(
                f"Put {card} back on top of your deck?",
                (f"Discard {card}", False),
                (f"Keep {card} on top of your deck", True),
            ):
                player.add_card(card, Piles.TOPDECK)
            else:
                player.discard_card(card)

        while player.piles[Piles.HAND].size() < 5:
            player.pickup_cards(1)

        cards = [_ for _ in player.piles[Piles.HAND] if not _.isTreasure()]
        if cards:
            player.plr_trash_card(cardsrc=cards, prompt="Trash a non-Treasure")


###############################################################################
class Test_Jack_of_all_Trades(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Jack of all Trades"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Jack of all Trades")

    def test_play(self) -> None:
        """Play a Jack of all Trades"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Copper", "Copper", "Gold")
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.test_input = ["keep", "duchy"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)

        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])  # Gain a Silver

        self.assertIn("Gold", self.plr.piles[Piles.HAND])  # Keep on deck, then picked up

        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 - 1)  # One trashed
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Duchy", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
