#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Acolyte"""

import unittest
from dominion import Game, Card, Piles


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
        self.pile = "Augurs"

    def special(self, game, player):
        options = [("Do nothing", None)]
        for card in player.piles[Piles.HAND]:
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
class TestAcolyte(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Augurs"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        self.card = self.g.get_card_from_pile("Augurs", "Acolyte")

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Estate", self.plr.piles[Piles.HAND])

    def test_trash_self(self):
        """Play the card and trash self"""
        self.g.card_piles["Augurs"].rotate()  # Acolytes top
        self.g.card_piles["Augurs"].rotate()  # Sorceress top

        self.plr.piles[Piles.HAND].set("Estate", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash self"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Acolyte", self.g.trash_pile)
        self.assertIn("Sorceress", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
