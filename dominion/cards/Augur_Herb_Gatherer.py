#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Herb_Gatherer"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Herb_Gatherer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.AUGUR]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 3
        self.buys = 1
        self.name = "Herb Gatherer"
        self.desc = """+1 Buy; Put your deck into your discard pile.
            Look through it and you may play a Treasure from it.
            You may rotate the Augurs."""
        self.pile = "Augurs"

    def special(self, game, player):
        for crd in player.piles[Piles.DECK]:
            player.move_card(crd, "discard")
            player.output(f"Discarding {crd.name} from deck")
        treasures = []
        for crd in player.piles[Piles.DISCARD]:
            if crd.isTreasure():
                treasures.append(crd)
        if treasures:
            options = []
            already = set()
            for treas in treasures:
                if treas.name not in already:
                    already.add(treas.name)
                    options.append((f"Play {treas.name}?", treas))
            choice = player.plr_choose_options("Play a treasure?", *options)
            player.move_card(choice, Piles.HAND)
            player.play_card(choice, cost_action=False)

        opt = player.plr_choose_options(
            "Do you want to rotate the Augurs?",
            ("Don't change", False),
            ("Rotate", True),
        )
        if opt:
            game["Augurs"].rotate()


###############################################################################
class Test_Herb_Gatherer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Augurs"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g.get_card_from_pile("Augurs")
            if card.name == "Herb Gatherer":
                break
        self.card = card

    def test_play(self):
        """Play a card"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play Gold", "Don't change"]
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
