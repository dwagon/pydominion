#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Secret_Chamber """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Secretchamber(Card.Card):
    """TODO"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """Discard any number of cards; +1 coin per card discarded.
            When another player plays an Attack card, you may reveal
            this from you hand. If you do +2 cards, then put 2 cards
            from your hand on top of your deck """
        self.name = "Secret Chamber"
        self.cost = 2

    def special(self, game, player):  # pylint: disable=unused-argument
        """Discard any number of cards, +1 coin per card discarded"""
        todiscard = player.plr_discard_cards(
            any_number=True, prompt="Select which card(s) to discard (+1 coin per discard)?"
        )
        player.coins.add(len(todiscard))

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
            player.piles[Piles.HAND].remove(card)

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
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_play_three(self):
        """Play the Secret Chamber - discard three"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Province", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = [
            "discard copper",
            "discard silver",
            "discard gold",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.coins.get(), 3)

    def test_underattack(self):
        """Secret chamber is under attack - use it"""
        mil = self.g["Militia"].remove()
        self.plr.piles[Piles.DECK].set("Duchy", "Province")
        self.att.add_card(mil, Piles.HAND)
        self.plr.piles[Piles.HAND].set("Secret Chamber", "Silver", "Gold")
        self.plr.test_input = ["Reveal", "Put Silver", "Put Gold", "Finish"]
        self.att.play_card(mil)
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertNotIn("Province", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertNotIn("Silver", self.plr.piles[Piles.HAND])

    def test_underattack_pass(self):
        """Secret chamber is under attack - use it"""
        mil = self.g["Militia"].remove()
        self.plr.piles[Piles.DECK].set("Duchy", "Province")
        self.att.add_card(mil, Piles.HAND)
        self.plr.piles[Piles.HAND].set("Secret Chamber", "Silver", "Gold")
        self.plr.test_input = ["nothing"]
        self.att.play_card(mil)
        self.assertIn("Province", self.plr.piles[Piles.DECK])
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
