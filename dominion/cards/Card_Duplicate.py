#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Duplicate"""
import unittest
from typing import Any, Optional

from dominion import Game, Card, Piles, Player, Whens, OptionKeys, NoCardException


###############################################################################
class Card_Duplicate(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "When you gain a card costing up to 6, you may call this to gain a copy of that card"
        self.name = "Duplicate"
        self.cost = 4
        self.when = Whens.SPECIAL
        self._duplicate: Optional[Card.Card] = None

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if self not in player.piles[Piles.RESERVE]:
            return {}
        if card.cost > 6 or not card.purchasable or card.potcost:
            return {}
        if player.plr_choose_options(
            f"Call Duplicate on {card}?",
            ("Save for later", False),
            (f"Duplicate {card}", True),
        ):
            self._duplicate = card
            player.call_reserve(self)
        else:
            self._duplicate = None
        return {}

    def hook_call_reserve(self, game: Game.Game, player: Player.Player) -> None:
        card = self._duplicate
        assert card is not None
        player.output(f"Gaining a {card} from Duplicate")
        try:
            player.gain_card(card.name, callhook=False)
        except NoCardException:
            player.output(f"No more {card} left")


###############################################################################
class TestDuplicate(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Duplicate"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Duplicate")

    def test_buy(self) -> None:
        """Call Duplicate from reserve"""
        self.plr.coins.set(6)
        self.plr.piles[Piles.RESERVE].set("Duplicate")
        self.plr.test_input = ["Gold"]
        self.plr.buy_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for i in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(i.name, "Gold")
        self.assertEqual(self.plr.coins.get(), 0)

    def test_buy_non_reserve(self) -> None:
        """Buy a card when duplicate just in hand"""
        self.plr.coins.set(6)
        self.plr.piles[Piles.RESERVE].set()
        self.plr.piles[Piles.HAND].set("Duplicate")
        self.plr.buy_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
