#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Sextant"""
import unittest

from dominion import Loot, Card, Piles, NoCardException, Game, Player


###############################################################################
class Loot_Sextant(Loot.Loot):
    """Sextant"""

    def __init__(self) -> None:
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """$3; +1 Buy; Look at the top 5 cards of your deck. Discard any number.
        Put the rest back in any order."""
        self.name = "Sextant"
        self.purchasable = False
        self.coin = 3
        self.buys = 1
        self.cost = 7
        self.pile = "Loot"

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Look at the top 5 cards of your deck. Discard any number. Put the rest back in any order."""
        cards: list[Card.Card] = []
        for _ in range(5):
            try:
                card = player.next_card()
            except NoCardException:
                break
            cards.append(card)

        if to_discard := player.card_sel(
            prompt="Pick cards to discard", anynum=True, cardsrc=cards
        ):
            for card in cards:
                if card in to_discard:
                    player.add_card(card, Piles.DISCARD)
                else:
                    player.add_card(card, Piles.DECK)


###############################################################################
class TestSextant(unittest.TestCase):
    """Test Sextant"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Sextant":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_playing(self) -> None:
        """Test playing a doubloon"""
        self.plr.piles[Piles.DECK].set(
            "Copper", "Silver", "Gold", "Province", "Duchy", "Estate"
        )
        sextant = self.g.get_card_from_pile("Loot", "Sextant")
        self.plr.add_card(sextant, Piles.HAND)
        self.plr.test_input = [
            "Select Duchy",
            "Select Estate",
            "Select Province",
            "Finish",
        ]
        self.plr.play_card(sextant)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
