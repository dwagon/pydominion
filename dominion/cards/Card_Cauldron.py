#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Cauldron"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Cauldron(Card.Card):
    """Cauldron"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """$2; +1 Buy; The third time you gain an Action this turn,
            each other player gains a Curse."""
        self.name = "Cauldron"
        self.cost = 5
        self.coin = 2
        self.buys = 1
        self.required_cards = ["Curse"]

    def hook_gain_card(self, game, player, card):
        """The third time you gain an Action this turn, each other player gains a Curse."""
        actions = [_ for _ in player.stats["gained"] if _.isAction()]
        # Card just gained hasn't been added to the stats["gained"] until after hook
        if not card.isAction():
            return
        print(f"Actions={actions}")
        if len(actions) == 2:
            for pl in player.attack_victims():
                player.output(f"{pl.name} got cursed")
                pl.output(f"{player.name}'s Cauldron cursed you")
                pl.gain_card("Curse")


###############################################################################
class Test_Cauldron(unittest.TestCase):
    """Test Cauldron"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Cauldron", "Moat"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Cauldron")
        self.plr.add_card(self.card, "played")

    def test_play(self):
        """Play the Cauldron"""
        for _ in range(3):
            self.plr.gain_card("Moat")
        self.assertIn("Curse", self.oth.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
