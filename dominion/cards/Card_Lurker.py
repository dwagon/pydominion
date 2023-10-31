#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Lurker(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+1 Action; Choose one: Trash an Action card from the Supply, 
        or gain an Action card from the trash."""
        self.name = "Lurker"
        self.cost = 2
        self.actions = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.plr_choose_options(
            "Choose one? ",
            ("Trash an Action from the Supply", True),
            ("Gain an Action card from the Trash", False),
        ):
            self._trash_supply(game, player)
        else:
            self._from_trash(game, player)

    def _trash_supply(self, game: "Game.Game", player: "Player.Player") -> None:
        """Trash an action from supply"""
        options = []
        for name, pile in game.get_card_piles():
            if pile.is_empty():
                continue
            card = game.card_instances[name]
            if card.isAction():
                options.append((f"Trash {name}", name))

        if not options:
            player.output("No suitable cards found")
            return
        to_trash = player.plr_choose_options(
            "Select Action from Supply to Trash", *options
        )
        card = game.get_card_from_pile(to_trash)
        player.add_card(card, Piles.PLAYED)  # In order to trash
        player.trash_card(card)

    def _from_trash(self, game: "Game.Game", player: "Player.Player") -> None:
        """Gain an action from the trash"""
        acts = [_ for _ in game.trash_pile if _.isAction()]
        if not acts:
            player.output("No suitable cards found")
            return
        cards = player.card_sel(cardsrc=acts, prompt="Select Action from the Trash")
        if cards is not None:
            game.trash_pile.remove(cards[0])
            player.add_card(cards[0], Piles.DISCARD)


###############################################################################
class TestLurker(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Lurker", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Lurker")
        self.plr.add_card(self.card, Piles.HAND)

    def test_trash(self) -> None:
        self.plr.test_input = ["Trash an Action", "Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.g.trash_pile)
        self.assertEqual(self.plr.actions.get(), 0 + 1)

    def test_recover(self) -> None:
        self.plr.test_input = ["Gain an Action", "Moat"]
        self.g.trash_pile.set("Moat")
        self.plr.play_card(self.card)
        self.assertNotIn("Moat", self.g.trash_pile)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
