#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles, Player, NoCardException


###############################################################################
class Card_Zombie_Mason(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ZOMBIE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Trash the top card of your deck. You may gain a card costing up to 1 more than it."
        self.name = "Zombie Mason"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game: Game.Game) -> None:
        game.trash_pile.add(self)
        self.location = Piles.TRASH

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            topdeck = player.top_card()
        except NoCardException:
            player.output("No more cards in deck")
            return
        player.trash_card(topdeck)
        player.output(f"Trashed {topdeck} from the top of your deck")
        player.plr_gain_card(topdeck.cost + 1)


###############################################################################
class Test_Zombie_Mason(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Zombie Mason", "Guide"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Zombie Mason")

    def test_play(self) -> None:
        self.plr.piles[Piles.DECK].set("Estate")
        self.plr.test_input = ["Guide"]
        self.plr.play_card(self.card, discard=False, cost_action=False)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertIn("Guide", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
