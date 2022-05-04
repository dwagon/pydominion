#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Villain(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.RENAISSANCE
        self.name = "Villain"
        self.desc = "+2 Coffers; Each other player with 5 or more cards in hand discards one costing 2 or more (or reveals they can't)."
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        player.add_coffer(2)
        for vic in player.attack_victims():
            if vic.hand.size() >= 5:
                from_cards = []
                for card in vic.hand:
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
                    for card in vic.hand:
                        vic.reveal_card(card)
            else:
                player.output(f"{vic.name}'s hand size is too small")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # oragma: no cover
    # Discard a victory card first, then whichever
    for card in kwargs["cardsrc"]:
        if card.isVictory():
            return [card]
    return [kwargs["cardsrc"][0]]


###############################################################################
class Test_Villain(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, initcards=["Villain"], numhexes=0, numboons=0
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Villain"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_card(self):
        sc = self.plr.get_coffers()
        self.vic.set_hand("Gold", "Province", "Copper", "Copper", "Copper")
        self.vic.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coffers(), sc + 2)
        self.assertIn("Province", self.vic.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
