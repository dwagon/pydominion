#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card
from dominion.Player import Phase


###############################################################################
class Card_Exorcist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "Trash a card from your hand. Gain a cheaper Spirit from one of the Spirit piles."
        )
        self.name = "Exorcist"
        self.cost = 4
        self.required_cards = [
            ("Card", "Ghost"),
            ("Card", "Imp"),
            ("Card", "Will-o'-Wisp"),
        ]

    def night(self, game, player):
        if player.hand.is_empty():
            player.output("No cards to trash")
            return
        trashed = player.plr_trash_card(prompt="Trash a card and gain a cheaper spirit")
        if not trashed:
            return
        cost = trashed[0].cost
        options = []
        idx = 0
        for card in ("Ghost", "Imp", "Will-o'-Wisp"):
            if game[card].cost < cost:
                sel = f"{idx}"
                toprint = f"Get {card}"
                options.append({"selector": sel, "print": toprint, "card": card})
                idx += 1
        if idx:
            o = player.user_input(options, "Gain a spirit")
            player.gain_card(o["card"])
        else:
            player.output("No spirits available at that price")


###############################################################################
class Test_Exorcist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Exorcist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Exorcist"].remove()

    def test_play(self):
        self.plr.phase = Phase.NIGHT
        self.plr.hand.set("Silver", "Gold", "Province")
        self.plr.test_input = ["Silver", "Imp"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIn("Imp", self.plr.discardpile)
        self.assertIn("Silver", self.g.trashpile)
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
