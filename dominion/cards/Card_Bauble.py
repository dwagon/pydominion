#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


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
        deck = player.plrChooseOptions(
            "Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of deck" % card.name, True),
        )
        if deck:
            player.output("Putting %s on deck due to Royal Seal" % card.name)
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
            choice = player.plrChooseOptions("Choose an option.", *options)
            chosen.append(choice)
        for choice in chosen:
            if choice == "buy":
                player.add_buys(1)
            elif choice == "cash":
                player.addCoin(1)
            elif choice == "favor":
                player.add_favors(1)
            elif choice == "deck":
                self._gain_hook = True
            else:
                raise Exception(f"Unsupported {choice=}")


###############################################################################
class Test_Bauble(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Bauble"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Bauble"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_buy_cash(self):
        """Play the card and gain a buy and cash"""
        self.plr.test_input = ["buy", "cash"]
        self.plr.setBuys(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_coins(), 1)

    def test_play_cash_favor(self):
        """Play the card and gain a cash and favor"""
        self.plr.test_input = ["favor", "cash"]
        self.plr.setFavor(0)
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
