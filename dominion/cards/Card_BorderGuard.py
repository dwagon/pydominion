#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_BorderGuard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """+1 Action; Reveal the top 2 cards of your deck.
            Put one into your hand and discard the other. If both were Actions,
            take the Lantern or Horn."""
        self.name = "Border Guard"
        self.cost = 2
        self.actions = 1

    def special(self, game, player):
        ncards = 3 if player.has_artifact("Lantern") else 2
        cards = []
        for _ in range(ncards):
            card = player.next_card()
            player.reveal_card(card)
            cards.append(card)
        nacts = sum([1 for _ in cards if _.isAction()])
        ch = player.card_sel(
            prompt="Select a card to put into your hand, other will be discarded",
            cardsrc=cards,
        )
        player.add_card(ch[0], "hand")
        cards.remove(ch[0])
        for card in cards:
            player.output(f"Putting {card.name} into the discard pile")
            player.add_card(card, "discard")

        if nacts == ncards:
            art = player.plr_choose_options(
                "Pick an artifact to take",
                ("Take Lantern (Border Guard reveals 3 cards)", "Lantern"),
                ("Take Horn (May put discarded Border Guard into hand)", "Horn"),
            )
            player.assign_artifact(art)

    def hook_discard_this_card(self, game, player, source):
        if not player.has_artifact("Horn"):
            return
        ch = player.plr_choose_options(
            "Use Horn and put Border Guard onto deck?",
            ("Put onto deck", True),
            ("Keep in discard", False),
        )
        if ch:
            player.move_card(self, "topdeck")


###############################################################################
class Test_BorderGuard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Border Guard", "Moat", "Guide"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Border Guard"].remove()

    def test_play(self):
        self.plr.deck.set("Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Select Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Silver", self.plr.discardpile)

    def test_play_actions(self):
        self.plr.deck.set("Moat", "Guide")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Select Moat", "Take Horn"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.hand)
        self.assertIn("Guide", self.plr.discardpile)
        self.assertTrue(self.plr.has_artifact("Horn"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
