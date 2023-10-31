#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Imp(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SPIRIT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+2 Cards; You may play an Action card from your hand that you don't have a copy of in play."
        self.name = "Imp"
        self.purchasable = False
        self.insupply = False
        self.cards = 2
        self.cost = 2
        self.numcards = 13

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        # Get action cards in hand
        ac = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not ac:
            player.output("No action cards")
            return
        # Select ones that haven't been played
        sac = [_ for _ in ac if _.name not in player.piles[Piles.PLAYED]]
        if not sac:
            player.output("No unplayed action cards")
            return
        options: list[dict[str, Any]] = [
            {"selector": "0", "print": "Nothing", "card": None}
        ]
        index = 1
        for p in sac:
            selector = f"{index}"
            toprint = f"Play {p.name} ({p.description(player)})"
            options.append({"selector": selector, "print": toprint, "card": p})
            index += 1
        o = player.user_input(options, "What card do you want to play?")
        if o["card"]:
            player.play_card(o["card"], cost_action=False)


###############################################################################
class Test_Imp(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Imp", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Imp")

    def test_played(self) -> None:
        self.plr.piles[Piles.HAND].set("Moat", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 2)

    def test_not_played(self) -> None:
        self.plr.piles[Piles.HAND].set("Moat", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), 2 + 2 + 1
        )  # 2 for moat, 2 for imp, 1 for hand


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
