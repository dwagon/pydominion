#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Animal_Fair"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException, PlayArea, Phase


###############################################################################
class Card_Animal_Fair(Card.Card):
    """Animal Fair"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Animal Fair"
        self.coin = 4
        self.always_buyable = True
        self.cost = 7

    def dynamic_description(self, player: "Player.Player") -> str:
        if player.phase == Phase.BUY:
            return """+4 Coin; +1 Buy per empty supply pile.
            Instead of paying this card's cost, you may trash an Action card
            from your hand."""
        return """+4 Coin; +1 Buy per empty supply pile."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        empties = sum(1 for _, stack in game.get_card_piles() if stack.is_empty())
        player.buys.add(empties)

    def hook_buy_this_card(self, game: "Game.Game", player: "Player.Player") -> None:
        # Fake cost modification by adding debt if required
        actions = PlayArea.PlayArea(initial=[_ for _ in player.piles[Piles.HAND] if _.isAction()])
        if not actions:
            adjust_debt(player)
            return
        if player.plr_trash_card(prompt="Trash an action card to get Animal Fair for free", num=1, cardsrc=actions):
            player.coins.add(7)
        else:
            adjust_debt(player)


###############################################################################
def adjust_debt(player: "Player.Player"):
    """Adjust coins if the player didn't trash an action"""
    if player.coins.get() < 0:
        player.output("Not enough coins - adding debt")
        player.debt.add(abs(player.coins.get()))
        player.coins.set(0)


###############################################################################
class TestAnimalFair(unittest.TestCase):
    """Test Animal Fair"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Animal Fair", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        """Play an Animal Fair"""
        card = self.g.get_card_from_pile("Animal Fair")
        self.plr.add_card(card, Piles.HAND)
        while True:  # Empty pile
            try:
                self.g.get_card_from_pile("Moat")
            except NoCardException:
                break
        self.plr.play_card(card)
        self.assertEqual(self.plr.coins.get(), 4)
        self.assertEqual(self.plr.buys.get(), 1 + 1)

    def test_buy_no_action_card(self) -> None:
        """Buy an Animal Fair and trash an action"""
        self.plr.coins.set(0)
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.buy_card("Animal Fair")
        self.assertNotIn("Moat", self.g.trash_pile)
        self.assertEqual(self.plr.debt.get(), 7)

    def test_buy_and_trash_card(self) -> None:
        """Buy an Animal Fair and trash an action"""
        self.plr.coins.set(5)
        self.plr.piles[Piles.HAND].set("Moat", "Copper")
        self.plr.test_input = ["Trash Moat"]
        self.plr.buy_card("Animal Fair")
        self.assertIn("Moat", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 5)

    def test_buy_no_trash_card(self) -> None:
        """Buy an Animal Fair and do not trash an action"""
        self.plr.coins.set(5)
        self.plr.piles[Piles.HAND].set("Moat", "Copper")
        self.plr.test_input = ["Finish"]
        self.plr.buy_card("Animal Fair")
        self.assertNotIn("Moat", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.debt.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
