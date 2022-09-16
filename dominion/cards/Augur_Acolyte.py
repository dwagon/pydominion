#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Acolyte"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Acolyte(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.AUGUR]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.name = "Acolyte"
        self.desc = """You may trash an Action or Victory card from your hand
            to gain a Gold.  You may trash this to gain an Augur."""

    def special(self, game, player):
        options = []
        options.append(("Do nothing", None))
        for card in player.hand:
            if card.isAction() or card.isVictory():
                options.append((f"Trash {card.name} to gain a Gold", card))
        options.append(("Trash self to gain an Augur", self))
        ans = player.plr_choose_options("Trash some cards?", *options)
        if not ans:
            return
        player.trash_card(ans)
        if ans == self:
            player.gain_card("Augurs")
        else:
            player.gain_card("Gold")


###############################################################################
class Test_Acolyte(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Augurs"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g["Augurs"].remove()
            if card.name == "Acolyte":
                break
        self.card = card

    def test_play(self):
        """Play the card"""
        self.plr.hand.set("Estate", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertNotIn("Estate", self.plr.hand)

    def test_trash_self(self):
        """Play the card and trash self"""
        self.g["Augurs"].rotate()
        self.plr.hand.set("Estate", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash self"]
        self.plr.play_card(self.card)
        self.assertIn("Acolyte", self.g.trashpile)
        self.assertIn("Sorceress", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
