#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sailor"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Sailor(Card.Card):
    """Sailor"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.SEASIDE
        self.desc = """+1 Action; Once this turn, when you gain a Duration card, you may play it.
            At the start of your next turn, +$2 and you may trash a card from your hand."""
        self.actions = 1
        self.name = "Sailor"
        self.cost = 4

    def hook_gain_card(self, game, player, card):
        """Once this turn, when you gain a Duration card, you may play it."""
        if not card.isDuration():
            return {}
        if player.do_once("Sailor"):
            to_play = player.plr_choose_options(
                f"Sailor lets you play {card.name} now",
                ("Don't play", False),
                ("Play now", True),
            )
            if to_play:
                player.move_card(card, "hand")
                player.output(f"Playing {card.name} from Sailor effect")
                player.play_card(card, costAction=False)
                return {"dontadd": True}
        return {}

    def duration(self, game, player):
        """At the start of your next turn, +$2 and you may trash a card from your hand."""
        player.add_coins(2)
        player.plr_trash_card(num=1)


###############################################################################
class Test_Sailor(unittest.TestCase):
    """Test Sailor"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sailor", "Guardian"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sailor"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a sailor"""
        self.plr.play_card(self.card)
        self.plr.test_input = ["Play now"]
        self.plr.gain_card("Guardian")
        self.assertIn("Guardian", self.plr.durationpile)
        self.assertIn("Sailor", self.plr.durationpile)
        self.plr.end_turn()
        self.plr.hand.set("Gold", "Silver", "Copper")
        self.plr.deck.set("Province")
        self.plr.test_input = ["Trash Copper"]
        self.plr.start_turn()
        self.g.print_state()
        self.assertEqual(self.plr.get_coins(), 3)  # 2 for sailor, 1 for guardian
        self.assertIn("Copper", self.g.trashpile)
        self.assertIn("Guardian", self.plr.played)
        self.assertIn("Sailor", self.plr.played)

    def test_play_no_duration(self):
        """Play a sailor but don't gain a duration card"""
        self.plr.play_card(self.card)
        self.plr.test_input = ["Play now"]
        self.plr.gain_card("Province")
        self.assertIn("Province", self.plr.discardpile)
        self.plr.hand.set("Gold", "Silver", "Copper")
        self.plr.test_input = ["Trash Copper"]
        self.plr.start_turn()
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIn("Copper", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
