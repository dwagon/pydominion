#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Rebuild(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 action. Name a card. Reveal cards from the top
        of your deck until you reveal a Victory card that is
        not the named card.  Discard the other cards.
        Trash the Victory card and gain a Victory card cost up to 3 more than it"""
        self.name = "Rebuild"
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """Name a card. Reveal cards from the top of your deck
        until you reveal a Victory card that is not the named card.
        Discard the other cards. Trash the Victory card and gain a
        Victory card cost up to 3 more than it"""
        guess = self._pick_victory_card(game, player)
        if not guess:
            return
        discards = []
        while True:
            card = player.next_card()
            player.reveal_card(card)
            if not card:
                break
            if card.isVictory() and guess != card.name:
                player.output(f"Found and trashing {card}")
                player.trash_card(card)
                player.plr_gain_card(
                    card.cost + 3, modifier="less", types={Card.CardType.VICTORY: True}
                )
                break
            player.output(f"Drew and discarded {card}")
            discards.append(card)
        for c in discards:
            player.discard_card(c)

    def _pick_victory_card(self, game, player):
        """Get the player to guess the victory card"""
        stacks = game.get_victory_piles()
        options = []
        for card in stacks:
            options.append((f"{card}", card))
        guess = player.plr_choose_options(
            "Guess a victory card - the next victory card that is not that will be upgraded",
            *options,
        )
        return guess


###############################################################################
class TestRebuild(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Rebuild"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Rebuild")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a rebuild"""
        trash_size = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["Province", "Get Duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
        self.assertIn("Estate", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
