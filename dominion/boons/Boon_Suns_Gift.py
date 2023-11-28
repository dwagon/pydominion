#!/usr/bin/env python

import unittest
from dominion import Boon, Card, Game, Piles, Player, NoCardException


###############################################################################
class Boon_Suns_Gift(Boon.Boon):
    def __init__(self) -> None:
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Look at the top 4 cards of your deck.
        Discard any number of them and put the rest back in any order."""
        self.name = "The Sun's Gift"
        self.purchasable = False

    def special(self, game: Game.Game, player: Player.Player) -> None:
        cards = []
        for _ in range(4):
            try:
                cards.append(player.next_card())
            except NoCardException:
                break
        to_discard = player.plr_discard_cards(
            prompt="Discard any number and the rest go back on the top of the deck",
            any_number=True,
            cardsrc=cards,
        )
        assert to_discard is not None
        for card in cards:
            if card not in to_discard:
                player.add_card(card, "topdeck")


###############################################################################
class TestSunsGift(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Sun's Gift":
                self.g.boons = [b]
                break

        self.card = self.g.get_card_from_pile("Bard")
        self.plr.add_card(self.card, Piles.HAND)

    def test_suns_gift(self) -> None:
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province", "Duchy", "Copper")
        self.plr.test_input = ["Province", "Duchy", "finish"]
        self.plr.play_card(self.card)
        try:
            self.assertIn("Silver", self.plr.piles[Piles.DECK])
            self.assertIn("Gold", self.plr.piles[Piles.DECK])
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Province"])
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Duchy"])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
