#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Phase, Player, NoCardException


###############################################################################
class Card_Exorcist(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Trash a card from your hand. Gain a cheaper Spirit from one of the Spirit piles."
        self.name = "Exorcist"
        self.cost = 4
        self.required_cards = [
            ("Card", "Ghost"),
            ("Card", "Imp"),
            ("Card", "Will-o'-Wisp"),
        ]

    def night(self, game: Game.Game, player: Player.Player) -> None:
        if player.piles[Piles.HAND].is_empty():
            player.output("No cards to trash")
            return
        trashed = player.plr_trash_card(prompt="Trash a card and gain a cheaper spirit")
        if not trashed:
            return
        cost = trashed[0].cost
        options: list[dict[str, Any]] = []
        idx = 0
        for card_name in ("Ghost", "Imp", "Will-o'-Wisp"):
            card = game.card_instances[card_name]
            if game.card_piles[card_name].is_empty():
                continue
            if card.cost < cost:
                options.append(
                    {
                        "selector": f"{idx}",
                        "print": f"Get {card_name}",
                        "card": card_name,
                    }
                )
                idx += 1
        if idx:
            o = player.user_input(options, "Gain a spirit")
            player.gain_card(o["card"])
        else:
            player.output("No spirits available at that price")


###############################################################################
class TestExorcist(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Exorcist"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Exorcist")

    def test_play(self) -> None:
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.HAND].set("Silver", "Gold", "Province")
        self.plr.test_input = ["Silver", "Imp"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Imp", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.g.trash_pile)
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
