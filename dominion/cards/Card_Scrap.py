#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Scrap"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Scrap(Card.Card):
    """Scrap"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Trash a card from your hand.
            Choose a different thing per coin it costs: +1 Card; +1 Action; +1 Buy;
            +1 Coin; gain a Silver; gain a Horse."""
        self.name = "Scrap"
        self.cost = 3
        self.required_cards = [("Card", "Horse")]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        trc = player.plr_trash_card(printcost=True, prompt="Trash a card from your hand for benefits")
        if not trc:  # pragma: no coverage
            return
        cost = min(6, player.card_cost(trc[0]))
        if not cost:
            return
        chosen: list[str] = []
        for _ in range(cost):
            choices = []
            if "card" not in chosen:
                choices.append(("+1 Card", "card"))
            if "action" not in chosen:
                choices.append(("+1 Action", "action"))
            if "buy" not in chosen:
                choices.append(("+1 Buy", "buy"))
            if "coin" not in chosen:
                choices.append(("+$1 Coin", "coin"))
            if "silver" not in chosen:
                choices.append(("Gain a Silver", "silver"))
            if "horse" not in chosen:
                choices.append(("Gain a Horse", "horse"))
            opt = player.plr_choose_options("Select one", *choices)
            do_scrap_options(player, opt)
            choices.append(opt)


###############################################################################
def do_scrap_options(player: Player.Player, opt: str) -> None:
    match opt:
        case "card":
            player.pickup_cards(1)
        case "action":
            player.add_actions(1)
        case "buy":
            player.buys.add(1)
        case "coin":
            player.coins.add(1)
        case "silver":
            try:
                player.gain_card("Silver")
            except NoCardException:  # pragma: no coverage
                player.output("No more Silvers")
        case "horse":
            try:
                player.gain_card("Horse")
            except NoCardException:  # pragma: no coverage
                player.output("No more Horses")


###############################################################################
class TestScrap(unittest.TestCase):
    """Test Scrap"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Scrap"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Scrap")

    def test_play_card_cost_0(self) -> None:
        """Play a scrap and trash something worth 0"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash copper", "finish"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)

    def test_play_card_cost_3(self) -> None:
        """Play a scrap and trash something worth 3"""
        self.plr.piles[Piles.HAND].set("Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.test_input = [
            "trash silver",
            "card",
            "finish",
            "action",
            "finish",
            "coin",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertIn("Silver", self.g.trash_pile)

    def test_play_card_cost_6(self) -> None:
        """Play a scrap and trash something worth more than 4"""
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Copper")
        self.plr.test_input = [
            "trash province",
            "card",
            "finish",
            "action",
            "finish",
            "coin",
            "finish",
            "buy",
            "finish",
            "silver",
            "finish",
            "horse",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trash_pile)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
