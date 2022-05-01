#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Bauble(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_LIAISON]
        self.base = Game.ALLIES
        self.name = "Bauble"
        self.desc = """Choose two different options: +1 Buy; +$1; +1 Favor;
                       this turn, when you gain a card, you may put it onto your deck."""
        self.cost = 2
        self._gain_hook = False

    def hook_gain_card(self, game, player, card):
        if not self._gain_hook:
            return {}
        mod = {}
        deck = player.plr_choose_options(
            f"Where to put {card.name}?",
            (f"Put {card.name} on discard", False),
            (f"Put {card.name} on top of deck", True),
        )
        if deck:
            player.output(f"Putting {card.name} on deck due to Royal Seal")
            mod["destination"] = "topdeck"
        return mod

    def special(self, game, player):
        self._gain_hook = False
        chosen = []
        player.output("Choose two different options")
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
        for choice in chosen:
            if choice == "buy":
                player.add_buys(1)
            elif choice == "cash":
                player.add_coins(1)
            elif choice == "favor":
                player.add_favors(1)
            elif choice == "deck":
                self._gain_hook = True
            else:
                raise Exception(f"Unsupported {choice=}")


###############################################################################
class Test_Bauble(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bauble"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Bauble"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_buy_cash(self):
        """Play the card and gain a buy and cash"""
        self.plr.test_input = ["buy", "cash"]
        self.plr.set_buys(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_coins(), 1)

    def test_play_cash_favor(self):
        """Play the card and gain a cash and favor"""
        self.plr.test_input = ["favor", "cash"]
        self.plr.set_favors(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_favors(), 1)
        self.assertEqual(self.plr.get_coins(), 1)

    def test_play_deck_deck(self):
        """Play the card and put next card on to deck"""
        self.plr.test_input = ["favor", "deck", "deck"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.deck[-1].name, "Gold")
        self.assertFalse(self.plr.in_discard("Gold"))

    def test_play_deck_discard(self):
        """Play the card and put next card on to deck"""
        self.plr.test_input = ["favor", "deck", "discard"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Gold")
        self.assertNotEqual(self.plr.deck[-1].name, "Gold")
        self.assertTrue(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
