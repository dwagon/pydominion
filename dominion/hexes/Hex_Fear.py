#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_Fear(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.TYPE_HEX
        self.base = Game.NOCTURNE
        self.desc = (
            "If you have at least 5 cards in hand, discard an Action or Treasure"
        )
        self.name = "Fear"
        self.purchasable = False

    def special(self, game, player):
        if player.hand.size() < 5:
            return
        tanda = [_ for _ in player.hand if _.isAction() or _.isTreasure()]
        player.plr_discard_cards(
            num=1, cardsrc=tanda, prompt="Discard an Action or a Treasure"
        )


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(1, keepvic=True)


###############################################################################
class Test_Fear(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Fear":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_empty_war(self):
        self.plr.set_hand("Estate", "Duchy", "Province", "Gold")
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.discardpile.size(), 1)  # The Cursed Village

    def test_war(self):
        self.plr.set_hand("Estate", "Duchy", "Estate", "Duchy", "Copper")
        self.plr.test_input = ["Copper"]
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertIsNotNone(self.plr.discardpile["Copper"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
