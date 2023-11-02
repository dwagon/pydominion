#!/usr/bin/env python

import contextlib
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Ironmonger(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 card, +1 action. Reveal the top card of your deck; you may
        discard it.  Either way, if it is an... Action card, +1 Action;
        Treasure Card, +1 coin; Victory Card, +1 card"""
        self.name = "Iron Monger"
        self.cost = 4
        self.actions = 1
        self.cards = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Reveal the top card of your deck; you may discard it.
        Either way, if it is an... Action card, +1 Action; Treasure
        Card, +1 coin; Victory Card, +1 card"""
        try:
            card = player.next_card()
        except NoCardException:
            return
        player.reveal_card(card)
        if player.plr_choose_options(
            f"What to do with {card}? ",
            (f"Put back {card}", False),
            (f"Discard {card}", True),
        ):
            player.discard_card(card)
        else:
            player.add_card(card, "topdeck")
        if card.isVictory():
            player.output(f"Picking up card as {card} was a victory card")
            with contextlib.suppress(NoCardException):
                player.pickup_card()
        if card.isAction():
            player.output(f"Gaining action as {card} was an action card")
            player.add_actions(1)
        if card.isTreasure():
            player.output(f"Gaining a coin as {card} was a treasure card")
            player.coins.add(1)


###############################################################################
class Test_Ironmonger(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Iron Monger"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.im = self.g.get_card_from_pile("Iron Monger")
        self.plr.add_card(self.im, Piles.HAND)

    def test_play(self) -> None:
        self.plr.test_input = ["put back"]
        self.plr.play_card(self.im)
        self.assertEqual(self.plr.actions.get(), 1)
        # 5 for hand, +1 for ironmonger and another potential +1 for action
        self.assertIn(self.plr.piles[Piles.HAND].size(), [6, 7])

    def test_victory(self) -> None:
        self.plr.test_input = ["put back"]
        self.plr.piles[Piles.DECK].set("Duchy", "Estate")
        self.plr.play_card(self.im)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_treasure(self) -> None:
        self.plr.test_input = ["put back"]
        self.plr.piles[Piles.DECK].set("Copper", "Gold")
        self.plr.play_card(self.im)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_action(self) -> None:
        self.plr.test_input = ["put back"]
        self.plr.piles[Piles.DECK].set("Iron Monger", "Iron Monger")
        self.plr.play_card(self.im)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_discard(self) -> None:
        self.plr.test_input = ["discard"]
        self.plr.piles[Piles.DECK].set("Iron Monger", "Gold")
        self.plr.play_card(self.im)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Iron Monger")

    def test_putback(self) -> None:
        self.plr.test_input = ["put back"]
        self.plr.piles[Piles.DECK].set("Copper", "Gold")
        self.plr.play_card(self.im)
        self.assertEqual(self.plr.piles[Piles.DECK][0].name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
