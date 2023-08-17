#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


class Card_Lookout(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Action; Look at the top 3 cards of your deck.
            Trash one of them. Discard one of them. Put the other one on top of
            your deck"""
        self.name = "Lookout"
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """Look at the top 3 cards of your deck. Trash one of them.
        Discard one of them. Put the other one on top of your deck
        """
        cards = []
        for _ in range(3):
            cards.append(player.next_card())
        cards = [_ for _ in cards if _]
        if not cards:
            player.output("No cards available")
            return
        player.output("Pulled %s from deck" % ", ".join([_.name for _ in cards]))
        player.output("Trash a card, discard a card, put a card on your deck")
        tc = self._trash(player, cards)
        cards.remove(tc)
        cd = self._discard(player, cards)
        cards.remove(cd)
        if cards:
            player.output(f"Putting {cards[0].name} on top of deck")
            player.add_card(cards[0], "topdeck")

    def _trash(self, player, cards):
        index = 1
        options = []
        for card in cards:
            index += 1
            options.append(
                {"selector": f"{index}", "print": f"Trash {card.name}", "card": card}
            )
        o = player.user_input(options, "Select a card to trash")
        player.trash_card(o["card"])
        return o["card"]

    def _discard(self, player, cards):
        index = 1
        options = []
        for card in cards:
            index += 1
            options.append(
                {"selector": f"{index}", "print": f"Discard {card.name}", "card": card}
            )
        o = player.user_input(options, "Select a card to discard")
        player.discard_card(o["card"])
        return o["card"]


###############################################################################
class TestLookout(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Lookout"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.lookout = self.g["Lookout"].remove()

    def test_actions(self):
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Gold", "Province")
        self.plr.add_card(self.lookout, Piles.HAND)
        self.plr.test_input = ["Province", "Gold"]
        self.plr.play_card(self.lookout)
        self.assertIn("Province", self.g.trashpile)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DECK][0].name, "Copper")
        self.assertEqual(self.plr.piles[Piles.DECK][1].name, "Estate")

    def test_no_cards(self):
        """Play a lookout when there are no cards available"""
        trash_size = self.g.trashpile.size()
        self.plr.piles[Piles.DECK].set()
        self.plr.add_card(self.lookout, Piles.HAND)
        self.plr.play_card(self.lookout)
        self.assertEqual(self.g.trashpile.size(), trash_size)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
