#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Black_Cat """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Black_Cat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_REACTION]
        self.base = Game.MENAGERIE
        self.desc = """+2 Cards; If it isn't your turn, each other player gains a
            Curse. When another player gains a Victory card, you may play this
            from your hand."""
        self.name = "Black Cat"
        self.cards = 2
        self.cost = 2
        self.required_cards = ["Curse"]

    def hook_allplayers_gain_card(self, game, player, owner, card):
        if owner == player:
            return
        if card.isVictory():
            for plr in owner.attackVictims():
                plr.output("{}'s Black Cat Cursed you".format(owner.name))
                plr.gain_card("Curse", callhook=False)


###############################################################################
class Test_Black_Cat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Black Cat"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g["Black Cat"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a card"""
        self.oth.gain_card("Estate")
        self.g.print_state()
        self.assertIsNotNone(self.oth.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
