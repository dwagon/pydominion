#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Tiara """
import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Tiara(Card.Card):
    """Tiara"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 Buy; This turn, when you gain a card, you may put it onto your deck.
        You may play a Treasure from your hand twice."""
        self.name = "Tiara"
        self.cost = 4
        self.buys = 1

    def special(self, game, player):
        """Play a treasure from your hand twice"""
        treasures = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treasures:
            return
        player.output("Select treasure that Tiara will let you play twice")
        if treasure := player.card_sel(cardsrc=treasures):
            for _ in range(2):
                player.play_card(treasure[0], discard=False, cost_action=False)
            player.move_card(treasure[0], Piles.DISCARD)

    def hook_gain_card(self, game, player, card):
        """when you gain a card, you may put it onto your deck."""
        if top_deck := player.plr_choose_options(
            f"Tiara lets you put {card} on top of your deck.",
            (f"Put {card} on top of your deck?", True),
            (f"Discard {card} as per normal?", False),
        ):
            return {"destination": "topdeck"}


###############################################################################
class TestTiara(unittest.TestCase):
    """Test Tiara"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Tiara"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Tiara")

    def test_play_deck(self):
        """Play a Tiara and put gained cards on to the deck"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.plr.test_input = ["Put"]
        self.plr.gain_card("Gold")
        self.assertIn("Gold", self.plr.piles[Piles.DECK])

    def test_discard(self):
        """Play a tiara and discard gained cards"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_treasure(self):
        """Play a tiara and play a treasure twice"""
        self.plr.piles[Piles.HAND].set("Copper", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Select Copper"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)  # Copper twice
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
