#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fools_Gold(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.REACTION]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """If this is the first time you played a Fool's Gold this turn, this is worth 1 Coin, otherwise it's worth 4 Coin.
        When another player gains a Province, you may trash this from your hand. If you do, gain a Gold, putting it on your deck."""
        self.name = "Fool's Gold"
        self.cost = 2

    def special(self, game, player):
        count = sum([1 for c in player.piles[Piles.PLAYED] if c.name == "Fool's Gold"])
        if count > 1:
            player.output("Gained 4 Coin")
            player.coins.add(4)
        else:
            player.output("Gained 1 Coin")
            player.coins.add(1)

    def hook_allplayers_gain_card(self, game, player, owner, card):
        if card.name != "Province":
            return
        if owner == player:
            return
        trash = owner.plr_choose_options(
            "%s gained a Province. Trash this card to gain a gold?" % player.name,
            ("Keep Fool's Gold", False),
            ("Trash and gain a Gold?", True),
        )
        if trash:
            owner.trash_card(self)
            owner.gain_card("Gold", destination="topdeck")


###############################################################################
class Test_Fools_Gold(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Fool's Gold"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Fool's Gold")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_once(self):
        """Play the Fools_Gold"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_play_twice(self):
        """Play the Fools_Gold again"""
        self.plr.piles[Piles.PLAYED].set("Fool's Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 4)

    def test_gain_province(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash"]
        self.other.gain_card("Province")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Fool's Gold", self.g.trash_pile)

    def test_self_gain_province(self):
        tsize = self.g.trash_pile.size()
        self.plr.gain_card("Province")
        self.assertNotEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertEqual(self.g.trash_pile.size(), tsize)
        self.assertNotIn("Fool's Gold", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
