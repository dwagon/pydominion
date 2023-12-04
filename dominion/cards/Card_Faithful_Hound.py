#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, Phase, PlayArea


###############################################################################
class Card_FaithfulHound(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """+2 Cards; When you discard this other than during Clean-up,
            you may set it aside, and put it into your hand at end of turn."""
        self.name = "Faithful Hound"
        self.cards = 2
        self.cost = 2

    def hook_discard_this_card(
        self, game: Game.Game, player: Player.Player, source: PlayArea.PlayArea
    ) -> None:
        if player.phase != Phase.CLEANUP:
            player.move_card(self, Piles.HAND)
            player.output("Faithful hound returns to your hand")


###############################################################################
class TestFaithfulHound(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Faithful Hound"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.plr._tracker_dont_boon = True
        self.card = self.g.get_card_from_pile("Faithful Hound")

    def test_play(self) -> None:
        """Play a Faithful Hound"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_discard(self) -> None:
        pass  # TODO


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
