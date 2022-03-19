#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Treasurer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.name = "Treasurer"
        self.desc = "+3 Coin; Choose one: Trash a Treasure from your hand; or gain a Treasure from the trash to your hand; or take the Key."
        self.cost = 5
        self.coin = 3
        self.needsartifacts = True

    ###########################################################################
    def special(self, game, player):
        gain_treas = [_ for _ in game.trashpile if _.isTreasure()]
        choice = player.plr_choose_options(
            "Choose one?",
            ("Trash a treasure from your hand", "trash"),
            (
                "Gain a treasure from the trash ({} available)".format(len(gain_treas)),
                "gain",
            ),
            ("Take the key", "key"),
        )
        if choice == "trash":
            treas = [_ for _ in player.hand if _.isTreasure()]
            player.plr_trash_card(cardsrc=treas)
        elif choice == "gain":
            card = player.card_sel(
                cardsrc=gain_treas, prompt="Select Treasure from the Trash"
            )
            if card:
                game.trashpile.remove(card[0])
                player.add_card(card[0], "hand")
        elif choice == "key":
            player.assign_artifact("Key")


###############################################################################
class Test_Treasurer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Treasurer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.plr.set_hand("Copper", "Silver")
        self.card = self.g["Treasurer"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_trash(self):
        self.plr.test_input = ["Trash a treasure", "Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertIsNotNone(self.g.in_trash("Silver"))

    def test_play_recover(self):
        self.g.set_trash("Gold", "Estate")
        self.plr.test_input = ["Gain a treasure", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertIsNone(self.g.in_trash("Gold"))
        self.assertIsNotNone(self.plr.in_hand("Gold"))

    def test_play_key(self):
        self.plr.test_input = ["Take the key"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertIsNotNone(self.plr.has_artifact("Key"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
