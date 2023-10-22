#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Mine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash a treasure, gain a better treasure"
        self.name = "Mine"
        self.cost = 5

    def _generate_options(self, player):
        """Generate the options for player dialog"""
        options = [{"selector": "0", "print": "Don't trash a card", "card": None}]
        index = 1
        for card in player.piles[Piles.HAND]:
            if card.isTreasure():
                options.append(
                    {
                        "selector": f"{index}",
                        "print": f"Trash/Upgrade {card.name}",
                        "card": card,
                    }
                )
                index += 1
        return options

    def special(self, game, player):
        """Trash a treasure card from your hand. Gain a treasure card
        costing up to 3 more, put it in your hand"""
        options = self._generate_options(player)
        player.output("Trash a treasure to gain a better one")
        o = player.user_input(options, "Trash which treasure?")
        if o["card"]:
            val = o["card"].cost
            # Make an assumption and pick the best treasure card
            # TODO - let user pick
            for card_name, _ in game.get_card_piles():
                card = game.get_card_from_pile(card_name)
                if not card:
                    continue
                if not card.isTreasure():
                    continue
                if card.cost == val + 3:
                    gained_card = player.gain_card(card_name, Piles.HAND)
                    if not gained_card:
                        player.output("No suitable cards left")
                        break
                    player.output(f"Converted to {gained_card.name}")
                    player.trash_card(o["card"])
                    break
            else:  # pragma: no cover
                player.output("No appropriate treasure card exists")


###############################################################################
class TestMine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mine")

    def test_convert_copper(self):
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Silver")
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.actions.get(), 0)

    def test_convert_nothing(self):
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Copper")
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
