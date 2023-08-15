#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Contraband"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Contraband(Card.Card):
    """Contraband"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+3 Coin +1 Buy. When you play this, the player to your left names a card.
            You can't buy that card this turn."""
        self.name = "Contraband"
        self.cost = 5
        self.coin = 3
        self.buys = 1

    def special(self, game, player):
        """When you play this, the player to your left names a card.
        You can't buy that card this turn."""
        plr = game.player_to_left(player)
        cps = [_ for _ in game.cardpiles if game.cardpiles[_].purchasable]
        options = []
        for cp in cps:
            options.append((cp, cp))
        forbid = plr.plr_choose_options(f"Contraband: Pick a stack that {player.name} can't buy this turn", *options)
        player.output(f"Forbidden to buy {forbid}")
        player.forbidden_to_buy.append(forbid)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """Bot response"""
    return "Province"


###############################################################################
class Test_Contraband(unittest.TestCase):
    """Test Contraband"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            oldcards=True,
            initcards=["Contraband"],
            badcards=["Fool's Gold"],
        )
        self.g.start_game()
        self.plr, self.nbr = self.g.player_list()
        self.card = self.g["Contraband"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Test play"""
        self.nbr.test_input = ["Gold"]
        self.plr.coins.set(6)
        self.plr.play_card(self.card)
        self.plr.phase = "buy"
        options, _ = self.plr._choice_selection()  # pylint: disable=protected-access
        for msg in options:
            if "Buy Gold" in msg["line"]:
                self.fail("Allowed to buy Gold")
        self.assertEqual(self.plr.coins.get(), 6 + 3)
        self.assertEqual(self.plr.buys.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
