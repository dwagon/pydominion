#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Crypt"""
import unittest

from dominion import Game, Piles, Card, PlayArea, Player, OptionKeys
from dominion.Player import Phase

CRYPT = "crypt"


###############################################################################
class Card_Crypt(Card.Card):
    """Crypt"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Set aside any number of non-Duration Treasures you have in play, face down (under this).
                    While any remain, at the start of each of your turns, put one of them into your hand."""
        self.name = "Crypt"
        self.cost = 5

    def night(self, game: Game.Game, player: Player.Player) -> None:
        if CRYPT not in player.specials:
            player.specials[CRYPT] = PlayArea.PlayArea(initial=[])
        relevant_cards = PlayArea.PlayArea(initial=[])
        for card in player.piles[Piles.PLAYED]:
            if card.isTreasure() and not card.isDuration():
                relevant_cards.add(card)
        if cards := player.card_sel(
            prompt="Set aside any number of Treasures you have in play",
            verbs=("Set", "Unset"),
            anynum=True,
            types={Card.CardType.TREASURE: True},
            cardsrc=relevant_cards,
        ):
            for card in cards:
                player.specials[CRYPT].add(card)
                player.piles[Piles.PLAYED].remove(card)
                player.secret_count += 1
            self.permanent = True

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        if CRYPT not in player.specials or player.specials[CRYPT].is_empty():
            return {}

        choices = [(f"Bring back {card}", card) for card in player.specials[CRYPT]]
        card = player.plr_choose_options("What card to bring back from the crypt?", *choices)
        player.add_card(card, Piles.HAND)
        player.specials[CRYPT].remove(card)
        player.secret_count -= 1
        if player.specials[CRYPT].is_empty():
            self.permanent = False
        return {}


###############################################################################
class TestCrypt(unittest.TestCase):
    """Test Crypt"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Crypt"], badcards=["Duchess"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Crypt")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play Crypt"""
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.PLAYED].set("Silver", "Gold", "Estate")
        self.plr.test_input = ["Set Gold", "Set Silver", "Finish"]
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Gold"]
        self.plr.start_turn()
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.specials[CRYPT]), 1)
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Silver"]
        self.plr.start_turn()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertFalse(self.card.permanent)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
