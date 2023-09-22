#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Herbalist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "+1 buy, +1 coin. When you discard this from play, you may put one of your Treasures from play on top of your deck"
        self.name = "Herbalist"
        self.cost = 2
        self.buys = 1
        self.coin = 1

    def hook_discard_this_card(self, game, player, source):
        """When you discard this from play, you may put one of
        your Treasures from play on top of your deck"""
        if source == "played":
            options = [{"selector": "0", "print": "Do nothing", "card": None}]
            index = 1
            player.output("Herbalist lets you put treasures on top of deck")
            for c in player.piles[Piles.PLAYED]:
                if c.isTreasure():
                    sel = "%d" % index
                    options.append({"selector": sel, "print": "Put %s" % c.name, "card": c})
                    index += 1
            print("index=%d" % index)
            if index != 1:
                o = player.user_input(options, "Put a card on the top of your deck?")
                if o["card"]:
                    player.piles[Piles.PLAYED].remove(o["card"])
                    player.add_card(o["card"], "topdeck")
            else:
                player.output("No suitable treasures = %s" % ",".join([c.name for c in player.piles[Piles.PLAYED]]))


###############################################################################
class Test_Herbalist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Herbalist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.hcard = self.g.get_card_from_pile("Herbalist")

    def test_putnothing(self):
        self.plr.piles[Piles.PLAYED].set("Gold", "Estate")
        self.plr.add_card(self.hcard, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.hcard)
        self.plr.discard_hand()
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 5)

    def test_putgold(self):
        self.plr.piles[Piles.PLAYED].set("Gold", "Estate")
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.hcard, Piles.HAND)
        self.plr.test_input = ["1"]
        self.plr.play_card(self.hcard)
        self.plr.discard_hand()
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Estate")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
