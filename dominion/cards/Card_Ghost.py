#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game, Piles
from dominion.Player import Phase


###############################################################################
class Card_Ghost(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.NIGHT,
            Card.CardType.DURATION,
            Card.CardType.SPIRIT,
        ]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Reveal cards from your deck until you reveal an Action.
            Discard the other cards and set aside the Action. At the start of
            your next turn, play it twice."""
        self.name = "Ghost"
        self.purchasable = False
        self.insupply = False
        self.cost = 4
        self._ghost_reserve = PlayArea.PlayArea([])

    def night(self, game, player):
        count = len(player.all_cards())
        while count:
            card = player.next_card()
            player.reveal_card(card)
            if card.isAction():
                self._ghost_reserve.add(card)
                player.secret_count += 1
                break
            player.add_card(card, "discard")
            count -= 1
        else:
            player.output("No action cards in deck")
            return

    def duration(self, game, player):
        for card in self._ghost_reserve:
            player.output(f"Ghost playing {card.name}")
            for _ in range(2):
                player.play_card(card, discard=False, cost_action=False)
            self._ghost_reserve.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_Ghost(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Ghost", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Ghost"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_with_no_actions(self):
        """Play a Ghost with no actions"""
        self.plr.phase = Phase.NIGHT
        self.plr.play_card(self.card)
        self.assertEqual(len(self.card._ghost_reserve), 0)

    def test_duration(self):
        try:
            self.plr.piles[Piles.DECK].set("Silver", "Gold", "Estate", "Silver", "Moat", "Copper")
            self.plr.piles[Piles.DISCARD].set("Silver", "Gold", "Estate", "Silver", "Moat", "Copper")
            self.plr.phase = Phase.NIGHT
            self.plr.play_card(self.card)
            self.plr.end_turn()
            self.plr.start_turn()
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2 * 2)  # Hand + Moat *2
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
