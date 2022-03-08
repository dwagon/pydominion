#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Herbalist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALCHEMY
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
            for c in player.played:
                if c.isTreasure():
                    sel = "%d" % index
                    options.append(
                        {"selector": sel, "print": "Put %s" % c.name, "card": c}
                    )
                    index += 1
            print("index=%d" % index)
            if index != 1:
                o = player.userInput(options, "Put a card on the top of your deck?")
                if o["card"]:
                    player.played.remove(o["card"])
                    player.addCard(o["card"], "topdeck")
            else:
                player.output(
                    "No suitable treasures = %s"
                    % ",".join([c.name for c in player.played])
                )


###############################################################################
class Test_Herbalist(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Herbalist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.hcard = self.g["Herbalist"].remove()

    def test_putnothing(self):
        self.plr.setPlayed("Gold", "Estate")
        self.plr.addCard(self.hcard, "hand")
        self.plr.test_input = ["0"]
        self.plr.playCard(self.hcard)
        self.plr.discardHand()
        self.assertEqual(self.plr.deck.size(), 5)

    def test_putgold(self):
        self.plr.setPlayed("Gold", "Estate")
        self.plr.hand.empty()
        self.plr.addCard(self.hcard, "hand")
        self.plr.test_input = ["1"]
        self.plr.playCard(self.hcard)
        self.plr.discardHand()
        self.assertEqual(self.plr.deck[-1].name, "Gold")
        self.assertEqual(self.plr.discardpile[-1].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertEqual(self.plr.deck.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
