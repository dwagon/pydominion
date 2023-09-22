#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Camel_Train """

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Camel_Train(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Camel Train"
        self.cost = 3

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """Exile a non-Victory card from the Supply. When you gain this, Exile a Gold from the Supply."""
        return "Exile a non-Victory card from the Supply."

    def special(self, game, player):
        options = []
        for name, pile in game.get_card_piles():
            if pile.is_empty():
                continue
            card = game.get_card_from_pile(name)
            if card.isVictory():
                continue
            if not card.purchasable:
                continue
            options.append((f"Exile {name}", name))

        to_exile = player.plr_choose_options("Pick a card to Exile", *options)
        if to_exile:
            player.exile_card(to_exile)

    def hook_gain_this_card(self, game, player):
        player.exile_card("Gold")


###############################################################################
class TestCamelTrain(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Camel Train"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Camel Train")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.test_input = ["Exile Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.EXILE])

    def test_gain(self):
        self.plr.gain_card("Camel Train")
        self.assertIn("Gold", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
