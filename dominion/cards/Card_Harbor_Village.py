#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Harbor_Village"""
import unittest

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_HarborVillage(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Card; +2 Actions; After the next Action you play this turn, if it gave you +$, +$1."""
        self.name = "Harbor Village"
        self.actions = 2
        self.cards = 1
        self.cost = 4

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        if not card.isAction():
            return {}
        if card.uuid == self.uuid:  # Don't trigger on playing self
            return {}
        if player.do_once(self.uuid):
            if card.coin != 0:
                player.output("Harbor Village adds 1 coin")
                player.coins.add(1)
        return {}


###############################################################################
class TestHarborVillage(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Harbor Village", "Moat", "Market"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Harbor Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card_no_coin(self) -> None:
        """Play Harbor Village and the next action has no coin value"""
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 2 - 1)
        moat = self.g.get_card_from_pile("Moat")
        coins = self.plr.coins.get()
        self.plr.play_card(moat)
        self.assertEqual(self.plr.coins.get(), coins)  # No effect for no cash gain

    def test_play_card_coin(self) -> None:
        """Play Harbor Village and the next action has a coin value"""
        self.plr.play_card(self.card)
        market = self.g.get_card_from_pile("Market")
        coins = self.plr.coins.get()
        copper = self.g.get_card_from_pile("Copper")
        self.plr.play_card(copper)
        self.assertEqual(self.plr.coins.get(), coins + 1)  # +1 Copper
        self.plr.play_card(market)
        self.assertEqual(self.plr.coins.get(), coins + 1 + 1 + 1)  # +1 Market, +1 Harbor V, +1 Copper


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
