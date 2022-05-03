#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Herb_Gatherer"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Herb_Gatherer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_AUGUR,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 3
        self.buys = 1
        self.name = "Herb Gatherer"
        self.desc = """+1 Buy; Put your deck into your discard pile.
            Look through it and you may play a Treasure from it.
            You may rotate the Augurs."""

    def special(self, game, player):
        for crd in player.deck[:]:
            player.move_card(crd, "discard")
        treasures = []
        for crd in player.discardpile:
            if crd.isTreasure():
                treasures.append(crd)
        if treasures:
            options = []
            already = set()
            for treas in treasures:
                if treas.name not in already:
                    already.add(treas.name)
                    options.append((f"Play {treas.name}?", treas))
            choice = player.plr_choose_options("Play a treasure?", **options)



###############################################################################
class Test_Herb_Gatherer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Augurs"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g["Augurs"].remove()
            if card.name == "Herb Gatherer":
                break
        self.card = card

    def test_play(self):
        """Play a card"""
        hndsz = self.plr.hand.size()
        self.plr.add_card(self.card, "hand")
        self.plr.set_discard("Estate", "Duchy", "Province", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.hand.size(), hndsz + 6)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
