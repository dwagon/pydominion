#!/usr/bin/env python

import unittest
from dominion import Card, Game, PlayArea


###############################################################################
class Card_Research(Card.Card):
    """Research"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Research"
        self.desc = """+1 Action; Trash a card from your hand.
            Per coin it costs, set aside a card from your deck face down.
            At the start of your next turn, put those cards into your hand."""
        self.cost = 4
        self.actions = 1
        self._research = PlayArea.PlayArea([])

    ###########################################################################
    def special(self, game, player):
        tc = player.plr_trash_card(num=1, force=True, printcost=True)
        cost = tc[0].cost
        if cost == 0:
            return
        cards = player.card_sel(
            prompt=f"Set aside {cost} cards for next turn",
            verbs=("Set", "Unset"),
            num=cost,
            cardsrc="hand",
        )
        for card in cards:
            self._research.add(card)
            player.hand.remove(card)
            player.secret_count += 1

    ###########################################################################
    def duration(self, game, player):
        cards = []
        for card in self._research:
            cards.append(card)
        for card in cards:
            player.output(f"Bringing {card.name} out from research")
            player.add_card(card, "hand")
            self._research.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_Research(unittest.TestCase):
    """Test Research"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Research", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Research"].remove()
        self.plr.hand.set("Gold", "Silver", "Copper")
        self.plr.add_card(self.card, "hand")
        self.moat = self.g["Moat"].remove()
        self.plr.add_card(self.moat, "hand")

    def test_play_card(self):
        self.plr.test_input = ["Trash Moat", "Set Gold", "Set Silver", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Moat", self.g.trashpile)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Silver", self.plr.hand)
        self.assertIn("Gold", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
