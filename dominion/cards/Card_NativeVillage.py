#!/usr/bin/env python
# pylint: disable=protected-access

import unittest
from dominion import Card, Game, PlayArea, Piles, Player, NoCardException

NATIVE_VILLAGE = "native_village"


###############################################################################
class Card_NativeVillage(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.desc = """+2 Actions;
            Choose one: Set aside the top card of your deck face down on your
            Native Village mat; or put all the cards from your mat into your hand."""
        self.name = "Native Village"
        self.base = Card.CardExpansion.SEASIDE
        self.actions = 2
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if NATIVE_VILLAGE not in player.specials:
            player.specials[NATIVE_VILLAGE] = PlayArea.PlayArea([])
        player.output(
            f'Native Village contains: {", ".join(_.name for _ in player.specials[NATIVE_VILLAGE])}'
        )
        choice = player.plr_choose_options(
            "Choose One",
            (
                "Set aside the top card of your deck face down on your Native Village mat",
                "push",
            ),
            ("Put all the cards from your mat into your hand.", "pull"),
        )
        if choice == "push":
            try:
                card = player.next_card()
            except NoCardException:
                return
            player.specials[NATIVE_VILLAGE].add(card)
            player.output(f"Adding {card} to the Native Village")
            player.secret_count += 1
        else:
            self.pull_back(player)

    def hook_end_of_game(self, game: Game.Game, player: Player.Player) -> None:
        self.pull_back(player)

    def pull_back(self, player: Player.Player) -> None:
        for card in player.specials[NATIVE_VILLAGE]:
            player.output(f"Returning {card} from Native Map")
            player.add_card(card, Piles.HAND)
            player.specials[NATIVE_VILLAGE].remove(card)
            player.secret_count -= 1


###############################################################################
class TestNativeVillage(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Native Village"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Native Village")

    def test_play(self) -> None:
        self.plr.piles[Piles.DECK].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Set aside"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.specials[NATIVE_VILLAGE][0].name, "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Put all"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.secret_count, 0)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
