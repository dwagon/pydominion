#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_ZombieSpy(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ZOMBIE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Card; +1 Action; Look at the top card of your deck. Discard it or put it back."
        self.name = "Zombie Spy"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1
        self.cards = 1
        self.actions = 1

    def setup(self, game: Game.Game) -> None:
        game.trash_pile.add(self)

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            card = player.next_card()
        except NoCardException:
            return
        if player.plr_choose_options(
            "Discard your card?",
            (f"Keep {card} on your deck", False),
            (f"Discard {card}", True),
        ):
            player.add_card(card, Piles.DISCARD)
            player.output(f"Zombie Spy discarded your {card}")
        else:
            player.add_card(card, "topdeck")


###############################################################################
class TestZombieSpy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Zombie Spy"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Zombie Spy")

    def test_play_keep(self) -> None:
        assert self.card is not None
        self.plr.test_input = ["Keep"]
        self.plr.piles[Piles.DECK].set("Province", "Estate")
        self.plr.play_card(self.card, discard=False, cost_action=False)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertIn("Province", self.plr.piles[Piles.DECK])

    def test_play_discard(self) -> None:
        assert self.card is not None
        self.plr.test_input = ["Discard"]
        self.plr.piles[Piles.DECK].set("Province", "Estate")
        self.plr.play_card(self.card, discard=False, cost_action=False)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertNotIn("Province", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
