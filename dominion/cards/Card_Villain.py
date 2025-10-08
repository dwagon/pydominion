#!/usr/bin/env python

import unittest

from dominion import Game, Piles, Player, Card


###############################################################################
class Card_Villain(Card.Card):
    """Villain"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Villain"
        self.desc = """+2 Coffers; Each other player with 5 or more cards in hand discards one costing 2 or more
                (or reveals they can't)."""
        self.cost = 5

    ###########################################################################
    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        player.coffers.add(2)
        for vic in player.attack_victims():
            if vic.piles[Piles.HAND].size() >= 5:
                from_cards = []
                for card in vic.piles[Piles.HAND]:
                    if card.cost >= 2:
                        from_cards.append(card)
                if from_cards:
                    disc = vic.plr_discard_cards(
                        prompt=f"{player.name}'s Villain forcing you to discard one card",
                        cardsrc=from_cards,
                        num=1,
                    )
                    player.output(f"{vic.name} discarded {disc[0].name}")
                else:
                    player.output(f"{vic.name} had no appropriate cards")
                    for card in vic.piles[Piles.HAND]:
                        vic.reveal_card(card)
            else:
                player.output(f"{vic.name}'s hand size is too small")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # oragma: no cover, pylint: disable=unused-argument
    # Discard a victory card first, then whichever
    for card in kwargs["cardsrc"]:
        if card.isVictory():
            return [card]
    return [kwargs["cardsrc"][0]]


###############################################################################
class Test_Villain(unittest.TestCase):
    """Test Villain"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Villain"], numhexes=0, numboons=0)
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Villain")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        sc = self.plr.coffers.get()
        self.vic.piles[Piles.HAND].set("Gold", "Province", "Copper", "Copper", "Copper")
        self.vic.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coffers.get(), sc + 2)
        self.assertIn("Province", self.vic.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
