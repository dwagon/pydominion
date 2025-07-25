#!/usr/bin/env python

import unittest
from dominion import Game, Piles, Card, PlayArea
from dominion.Player import Phase


###############################################################################
class Card_Crypt(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Set aside any number of Treasures you have in play, face down
            (under this). While any remain, at the start of each of your turns,
            put one of them into your hand."""
        self.name = "Crypt"
        self.cost = 5
        self._crypt_reserve = PlayArea.PlayArea([])

    def night(self, game, player):
        if cards := player.card_sel(
            prompt="Set aside any number of Treasures you have in play",
            verbs=("Set", "Unset"),
            anynum=True,
            types={Card.CardType.TREASURE: True},
            cardsrc="played",
        ):
            for card in cards:
                self._crypt_reserve.add(card)
                player.piles[Piles.PLAYED].remove(card)
                player.secret_count += 1
            self.permanent = True

    def duration(self, game, player):
        if self._crypt_reserve.is_empty():
            return
        options = []
        index = 0
        for card in self._crypt_reserve:
            to_print = f"Bring back {card.name}"
            options.append({"selector": f"{index}", "print": to_print, "card": card})
            index += 1

        o = player.user_input(options, "What card to bring back from the crypt?")
        player.add_card(o["card"], Piles.HAND)
        self._crypt_reserve.remove(o["card"])
        player.secret_count -= 1
        if self._crypt_reserve.is_empty():
            self.permanent = False


###############################################################################
class TestCrypt(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Crypt"], badcards=["Duchess"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Crypt")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.PLAYED].set("Silver", "Gold", "Estate")
        self.plr.test_input = ["Set Gold", "Set Silver", "Finish"]
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Gold"]
        self.plr.start_turn()
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.card._crypt_reserve), 1)
        self.plr.end_turn()
        self.plr.test_input = ["Bring back Silver"]
        self.plr.start_turn()
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertFalse(self.card.permanent)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
