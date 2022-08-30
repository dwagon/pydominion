#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Teacher"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Teacher(Card.Card):
    """ Teacher """
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = """At the start of your turn, you may call this,
            to move your +1 Card, +1 Action, +1 Buy or +1 Coin token
            to an Action Supply pile you have no tokens on"""
        self.name = "Teacher"
        self.purchasable = False
        self.cost = 6
        self.numcards = 5

    def special(self, game, player):
        """At the start of your turn, you may call this, to move your +1 Card,
        +1 Action, +1 Buy or +1 Coin token to an Action Supply pile you have
        no tokens on"""
        for tkn in ("+1 Card", "+1 Action", "+1 Buy", "+1 Coin"):
            actionpiles = self.which_stacks(game, player)
            prompt = f"Which stack do you want to add the {tkn} token to?"
            if player.tokens[tkn]:
                prompt += f" Currently on {player.tokens[tkn]}"
            stacks = player.card_sel(num=1, prompt=prompt, cardsrc=actionpiles)
            if stacks:
                player.place_token(tkn, stacks[0].name)

    def which_stacks(self, game, player):
        """ Action piles which don't have the token """
        return [ap for ap in game.getActionPiles() if not player.which_token(ap.name)]


###############################################################################
class Test_Teacher(unittest.TestCase):
    """ Test Teacher """
    def setUp(self):
        initcards = [
            "Page",
            "Cellar",
            "Chapel",
            "Moat",
            "Village",
            "Harbinger",
            "Workshop",
            "Bureaucrat",
            "Gardens",
        ]
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=initcards)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Teacher"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """ Play the card """
        self.plr.test_input = ["Select Cellar", "Select Chapel", "Select Moat", "Select Village"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.tokens["+1 Card"], "Cellar")
        self.assertEqual(self.plr.tokens["+1 Action"], "Chapel")
        self.assertEqual(self.plr.tokens["+1 Buy"], "Moat")
        self.assertEqual(self.plr.tokens["+1 Coin"], "Village")

    def test_which_stacks(self):
        """ Test which_stacks() """
        orig_output = self.card.which_stacks(self.g, self.plr)
        for c in orig_output:
            if c.name == "Gardens":
                self.fail("Non action card in action card list")
        self.plr.place_token("+1 Card", "Moat")
        output = self.card.which_stacks(self.g, self.plr)
        self.assertEqual(len(output), len(orig_output) - 1)
        for c in output:
            if c.name == "Moat":
                self.fail("Card with token in action card list")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
