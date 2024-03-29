#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Border_Guard"""
import unittest
from dominion import Game, Card, Piles, Player, PlayArea, NoCardException


###############################################################################
class Card_BorderGuard(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+1 Action; Reveal the top 2 cards of your deck.
            Put one into your hand and discard the other. If both were Actions,
            take the Lantern or Horn."""
        self.name = "Border Guard"
        self.cost = 2
        self.actions = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        num_cards = 3 if player.has_artifact("Lantern") else 2
        cards: list[Card.Card] = []
        for _ in range(num_cards):
            try:
                card = player.next_card()
            except NoCardException:
                continue
            player.reveal_card(card)
            cards.append(card)
        num_acts = sum([1 for _ in cards if _.isAction()])
        ch = player.card_sel(
            prompt="Select a card to put into your hand, other will be discarded",
            cardsrc=cards,
        )
        if ch and ch[0] is not None:
            player.add_card(ch[0], Piles.HAND)
            cards.remove(ch[0])
        for card in cards:
            player.output(f"Putting {card} into the discard pile")
            player.add_card(card, "discard")

        if num_acts == num_cards:
            art = player.plr_choose_options(
                "Pick an artifact to take",
                ("Take Lantern (Border Guard reveals 3 cards)", "Lantern"),
                ("Take Horn (May put discarded Border Guard into hand)", "Horn"),
            )
            player.assign_artifact(art)

    def hook_discard_this_card(
        self, game: "Game.Game", player: "Player.Player", source: PlayArea.PlayArea
    ) -> None:
        if not player.has_artifact("Horn"):
            return
        ch = player.plr_choose_options(
            "Use Horn and put Border Guard onto deck?",
            ("Put onto deck", True),
            ("Keep in discard", False),
        )
        if ch:
            player.move_card(self, "topdeck")


###############################################################################
class Test_BorderGuard(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Border Guard", "Moat", "Guide"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Border Guard")

    def test_play(self) -> None:
        self.plr.piles[Piles.DECK].set("Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_actions(self) -> None:
        self.plr.piles[Piles.DECK].set("Moat", "Guide")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Moat", "Take Horn"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIn("Guide", self.plr.piles[Piles.DISCARD])
        self.assertTrue(self.plr.has_artifact("Horn"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
