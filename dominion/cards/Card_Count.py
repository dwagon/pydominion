#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Count(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """Choose one: Discard 2 cards; or put a card from your hand
            on top of your deck; or gain a Copper. Choose one: +3 Coin; or trash
            your hand; or gain a Duchy"""
        self.name = "Count"
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        """Choose one: Discard 2 cards; or put a card from your
        hand on top of your deck; or gain a copper.

        Choose one: +3 coin, or trash your hand or gain a Duchy"""

        ans = player.plr_choose_options(
            "What do you want to do?",
            ("Discard 2 cards", "discard"),
            ("Put a card from you hand on top of your deck", "putcard"),
            ("Gain a copper", "copper"),
        )
        if ans == "copper":
            player.output("Gained a copper")
            player.gain_card("Copper")
        elif ans == "putcard":
            self.putCard(game, player)
        else:
            player.plr_discard_cards(2)

        ans = player.plr_choose_options(
            "What do you want to do now?",
            ("+3 coin", "coin"),
            ("Trash hand", "trash"),
            ("Gain Duchy", "duchy"),
        )
        if ans == "duchy":
            player.output("Gained a duchy")
            player.gain_card("Duchy")
        elif ans == "trash":
            for c in player.hand[:]:
                player.output("Trashing %s" % c.name)
                player.trash_card(c)
        else:
            player.add_coins(3)

    ###########################################################################
    def putCard(self, game, player):
        """Put a card from your hand on top of your deck"""
        index = 1
        options = []
        for c in player.hand:
            sel = "%d" % index
            pr = "Put %s on top of your deck" % c.name
            options.append({"selector": sel, "print": pr, "card": c})
            index += 1
        o = player.user_input(options, "Select card to put on top of your deck")
        player.output("Moving %s to top of deck" % o["card"].name)
        player.add_card(o["card"], "topdeck")
        player.hand.remove(o["card"])


###############################################################################
class Test_Count(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Count"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Count"].remove()
        self.plr.set_hand("Copper", "Estate", "Silver", "Province", "Gold")

    def test_discard(self):
        self.plr.add_card(self.card, "hand")
        # Discard, select card 1 and card 2, finish selecting, +3 coin
        self.plr.test_input = [
            "discard 2",
            "discard estate",
            "discard copper",
            "finish",
            "+3 coin",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertEqual(self.plr.hand.size(), 3)

    def test_topdeck(self):
        self.plr.set_hand("Gold")
        self.plr.add_card(self.card, "hand")
        # top deck, card select, +3 coin
        self.plr.test_input = ["top of your deck", "put gold", "+3 coin"]
        self.plr.play_card(self.card)
        nc = self.plr.next_card()
        self.assertEqual(nc.name, "Gold")

    def test_gainCopper(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["gain a copper", "+3 coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_gaingold(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["gain a copper", "+3 coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)

    def test_trashhand(self):
        tsize = self.g.trashSize()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["gain a copper", "trash hand"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.hand.is_empty())
        self.assertEqual(self.g.trashSize(), tsize + 5)

    def test_gainDuchy(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["gain a copper", "gain duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile[1].name, "Duchy")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
