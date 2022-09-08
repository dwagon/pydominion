#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Secret_Chamber """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Secretchamber(Card.Card):
    """TODO"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.INTRIGUE
        self.desc = """Discard any number of cards; +1 coin per card discarded.
            When another player plays an Attack card, you may reveal
            this from you hand. If you do +2 cards, then put 2 cards
            from your hand on top of your deck """
        self.name = "Secret Chamber"
        self.cost = 2

    def special(self, game, player):  # pylint: disable=unused-argument
        """Discard any number of cards, +1 coin per card discarded"""
        todiscard = player.plr_discard_cards(
            anynum=True, prompt="Select which card(s) to discard (+1 coin per discard)?"
        )
        player.add_coins(len(todiscard))

    def hook_underAttack(self, game, player, attacker):  # pylint: disable=unused-argument
        """TODO"""
        player.output(f"Under attack from {attacker.name}")
        if not self.doRevealCard(player):
            return
        player.reveal_card(self)
        player.pickup_cards(2)
        player.output("Put two cards onto deck")
        cards = player.card_sel(
            prompt="Put which two cards on top of deck?",
            force=True,
            num=2,
            verbs=("Put", "Unput"),
        )
        for card in cards:
            player.add_card(card, "topdeck")
            player.hand.remove(card)

    def doRevealCard(self, player):
        """TODO"""
        options = [
            {"selector": "0", "print": "Do nothing", "reveal": False},
            {
                "selector": "1",
                "print": "Reveal for +2 cards then put 2 cards from you hand on top of your deck",
                "reveal": True,
            },
        ]
        o = player.user_input(options, "Reveal Secret Chamber?")
        return o["reveal"]


###############################################################################
class Test_Secretchamber(unittest.TestCase):
    """Test Secret Chamber"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Secret Chamber", "Militia"])
        self.g.start_game()
        self.plr, self.att = self.g.player_list()
        self.card = self.g["Secret Chamber"].remove()

    def test_play_none(self):
        """Play the Secret Chamber - discard none"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.get_coins(), 0)

    def test_play_three(self):
        """Play the Secret Chamber - discard three"""
        self.plr.hand.set("Copper", "Silver", "Gold", "Province", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = [
            "discard copper",
            "discard silver",
            "discard gold",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_coins(), 3)

    def test_underattack(self):
        """Secret chamber is under attack - use it"""
        mil = self.g["Militia"].remove()
        self.plr.deck.set("Duchy", "Province")
        self.att.add_card(mil, "hand")
        self.plr.hand.set("Secret Chamber", "Silver", "Gold")
        self.plr.test_input = ["Reveal", "Put Silver", "Put Gold", "Finish"]
        self.att.play_card(mil)
        self.assertIn("Province", self.plr.hand)
        self.assertIn("Duchy", self.plr.hand)
        self.assertNotIn("Province", self.plr.deck)
        self.assertIn("Gold", self.plr.deck)
        self.assertIn("Silver", self.plr.deck)
        self.assertNotIn("Silver", self.plr.hand)

    def test_underattack_pass(self):
        """Secret chamber is under attack - use it"""
        mil = self.g["Militia"].remove()
        self.plr.deck.set("Duchy", "Province")
        self.att.add_card(mil, "hand")
        self.plr.hand.set("Secret Chamber", "Silver", "Gold")
        self.plr.test_input = ["nothing"]
        self.att.play_card(mil)
        self.assertIn("Province", self.plr.deck)
        self.assertIn("Duchy", self.plr.deck)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Silver", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
