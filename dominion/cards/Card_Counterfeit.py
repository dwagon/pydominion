#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Counterfeit(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "+1 Coin, +1 Buy; May play a treasure twice and trash it"
        self.name = "Counterfeit"
        self.cost = 5
        self.coin = 1
        self.buys = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """When you play this, you may play a Treasure from your
        hand twice. If you do, trash that Treasure"""
        options = [{"selector": "0", "print": "Do nothing", "card": None}]
        index = 1
        for card in player.piles[Piles.HAND]:
            if card.isTreasure():
                options.append(
                    {
                        "selector": f"{index}",
                        "print": f"Play {card} twice",
                        "card": card,
                    }
                )
                index += 1

        if index == 1:
            return
        o = player.user_input(options, "What to do?")
        if not o["card"]:
            return
        for _ in range(2):
            player.play_card(o["card"], cost_action=False, discard=False)
        player.trash_card(o["card"])


###############################################################################
class Test_Counterfiet(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Counterfeit"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Counterfeit")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_no_treasures(self) -> None:
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.test_input, ["0"])

    def test_twice(self) -> None:
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.assertIn("Gold", self.g.trash_pile)
        # CF + 2 * Gold
        self.assertEqual(self.plr.coins.get(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
