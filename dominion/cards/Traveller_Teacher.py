#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Teacher"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Teacher(Card.Card):
    """Teacher"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
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
        for token in ("+1 Card", "+1 Action", "+1 Buy", "+1 Coin"):
            options = []
            for pile in game.get_action_piles():
                if player.which_token(pile):
                    continue
                options.append((f"Select {pile}", pile))
            prompt = f"Which stack do you want to add the {token} token to?"
            if player.tokens[token]:
                prompt += f" Currently on {player.tokens[token]}"
            stack = player.plr_choose_options(prompt, *options)
            if stack:
                player.place_token(token, stack)


###############################################################################
class TestTeacher(unittest.TestCase):
    """Test Teacher"""

    def setUp(self):
        init_cards = [
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
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=init_cards)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Teacher"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        self.plr.test_input = [
            "Select Cellar",
            "Select Chapel",
            "Select Moat",
            "Select Village",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.tokens["+1 Card"], "Cellar")
        self.assertEqual(self.plr.tokens["+1 Action"], "Chapel")
        self.assertEqual(self.plr.tokens["+1 Buy"], "Moat")
        self.assertEqual(self.plr.tokens["+1 Coin"], "Village")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
