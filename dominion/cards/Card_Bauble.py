#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Bauble(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.LIAISON]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Bauble"
        self.desc = """Choose two different options: +1 Buy; +$1; +1 Favor;
                       this turn, when you gain a card, you may put it onto your deck."""
        self.cost = 2
        self._gain_hook = False

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if not self._gain_hook:
            return {}
        mod = {}
        deck = player.plr_choose_options(
            f"Where to put {card}?",
            (f"Put {card} on discard", False),
            (f"Put {card} on top of deck", True),
        )
        if deck:
            player.output(f"Putting {card} on deck due to Bauble")
            mod[OptionKeys.DESTINATION] = Piles.TOPDECK
        return mod

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Choose two different options: +1 Buy; +$1; +1 Favor;this turn, when you gain a card,
        you may put it onto your deck."""
        self._gain_hook = False
        player.output("Choose two different options")
        chosen = choose_bauble_options(player)
        for choice in chosen:
            if choice == "buy":
                player.buys.add(1)
            elif choice == "cash":
                player.coins.add(1)
            elif choice == "favor":
                player.favors.add(1)
            elif choice == "deck":
                self._gain_hook = True
            else:
                raise Exception(f"Unsupported {choice=}")


###############################################################################
def choose_bauble_options(player: "Player.Player") -> list[str]:
    """Player to choose which two options to take"""
    chosen = []
    for _ in range(2):
        options = []
        if "buy" not in chosen:
            options.append(("+1 Buy", "buy"))
        if "cash" not in chosen:
            options.append(("+$1 cash", "cash"))
        if "favor" not in chosen:
            options.append(("+1 Favor", "favor"))
        if "deck" not in chosen:
            options.append(
                (
                    "This turn when you gain a card, you may put it onto your deck",
                    "deck",
                )
            )
        choice = player.plr_choose_options("Choose an option.", *options)
        chosen.append(choice)
    return chosen


###############################################################################
class TestBauble(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Bauble"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Bauble")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_buy_cash(self) -> None:
        """Play the card and gain a buy and cash"""
        self.plr.test_input = ["buy", "cash"]
        self.plr.buys.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_play_cash_favor(self) -> None:
        """Play the card and gain a cash and favor"""
        self.plr.test_input = ["favor", "cash"]
        self.plr.favors.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_play_deck_deck(self) -> None:
        """Play the card and put next card on to deck"""
        self.plr.test_input = ["favor", "deck", "deck"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertFalse(self.plr.piles[Piles.DISCARD]["Gold"])

    def test_play_deck_discard(self) -> None:
        """Play the card and put next card on to deck"""
        self.plr.test_input = ["favor", "deck", "discard"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Gold")
        self.assertNotEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertTrue(self.plr.piles[Piles.DISCARD]["Gold"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
