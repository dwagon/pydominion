#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Camel_Train """

import unittest
from dominion import Card, Game, Player


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
        cards = [_ for _ in game.cardpiles.values() if not _.isVictory() and not _.is_empty()]
        toex = player.card_sel(prompt="Pick a card to Exile", cardsrc=cards)
        if toex:
            player.exile_card(toex[0].name)

    def hook_gain_this_card(self, game, player):
        player.exile_card("Gold")


###############################################################################
class Test_Camel_Train(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Camel Train"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Camel Train"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.test_input = ["Select Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.exilepile)

    def test_gain(self):
        self.plr.gain_card("Camel Train")
        self.assertIn("Gold", self.plr.exilepile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
