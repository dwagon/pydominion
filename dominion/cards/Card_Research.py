#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, PlayArea, Player


###############################################################################
class Card_Research(Card.Card):
    """Research"""

    def __init__(self) -> None:
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
    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        tc = player.plr_trash_card(num=1, force=True, printcost=True)
        if tc is None:
            return
        cost = tc[0].cost
        if cost == 0:
            return
        cards = player.card_sel(
            prompt=f"Set aside {cost} cards for next turn",
            verbs=("Set", "Unset"),
            num=cost,
            cardsrc=Piles.HAND,
        )
        if not cards:
            return
        for card in cards:
            self._research.add(card)
            player.piles[Piles.HAND].remove(card)
            player.secret_count += 1

    ###########################################################################
    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[str, str] | None:
        cards = list(self._research)
        for card in cards:
            player.output(f"Bringing {card.name} out from research")
            player.add_card(card, Piles.HAND)
            self._research.remove(card)
            player.secret_count -= 1
        return None


###############################################################################
class TestResearch(unittest.TestCase):
    """Test Research"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Research", "Moat"], badcards=["Shaman"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Research")
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(self.moat, Piles.HAND)

    def test_play_card(self) -> None:
        self.plr.test_input = ["Trash Moat", "Set Gold", "Set Silver", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Moat", self.g.trash_pile)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
