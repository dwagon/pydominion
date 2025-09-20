#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_OldWitch(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+3 Cards; Each other player gains a Curse and may trash a Curse from their hand."""
        self.required_cards = ["Curse"]
        self.cards = 3
        self.name = "Old Witch"
        self.cost = 5

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        for victim in player.attack_victims():
            try:
                victim.gain_card("Curse")
                player.output(f"{victim} got cursed")
                victim.output(f"{player}'s Old Witch cursed you")
            except NoCardException:
                player.output("No more Curses")
            if tr := victim.piles[Piles.HAND]["Curse"]:
                if victim.plr_trash_card(cardsrc=[tr], prompt="You may trash a Curse"):
                    player.output(f"{victim} trashed a Curse")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return kwargs["cardsrc"]


###############################################################################
class TestOldWitch(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Old Witch"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Old Witch")

    def test_play(self) -> None:
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])

    def test_has_curse(self) -> None:
        self.vic.piles[Piles.HAND].set("Curse")
        self.plr.add_card(self.card, Piles.HAND)
        self.vic.test_input = ["Trash Curse"]
        self.plr.play_card(self.card)
        self.assertNotIn("Curse", self.vic.piles[Piles.HAND])
        self.assertIn("Curse", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
