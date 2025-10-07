#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Masquerade"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Masquerade(Card.Card):
    """Masquerade"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+2 Cards; Each player with any cards in hand passes one to the next such player to
        their left, at once. Then you may trash a card from your hand."""
        self.name = "Masquerade"
        self.cards = 2
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each player passes a card from his hand to the left at
        once. Then you may trash a card from your hand"""
        players = suitable_players(game)
        # Pick cards to give
        xfer = {}
        for plr in players:
            recipient = plr_to_left(players, plr)
            xfer[plr] = plr.card_sel(
                prompt=f"Due to {player}'s Masquerade: Which card to give to {recipient}?", num=1, force=True
            )[0]

        for plr in players:
            recipient = plr_to_left(players, plr)
            card = xfer[plr]
            plr.output(f"Gave {card} to {recipient}")
            plr.piles[Piles.HAND].remove(card)
            card.player = recipient
            recipient.output(f"You received a {card} from {plr}")
            recipient.add_card(card, Piles.HAND)

        player.plr_trash_card()


###############################################################################
def suitable_players(game: Game.Game) -> list[Player.Player]:
    return [_ for _ in game.player_list() if len(_.piles[Piles.HAND]) > 0]


###############################################################################
def plr_to_left(players: list[Player.Player], plr: Player.Player) -> Player.Player:
    return players[(players.index(plr) - 1) % len(players)]


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    c = player.pick_to_discard(1, keepvic=True)
    return c


###############################################################################
class TestMasquerade(unittest.TestCase):
    """Test Masquerade"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=3, initcards=["Masquerade"])
        self.g.start_game()
        self.plr, self.other, self.third = self.g.player_list()
        self.card = self.g.get_card_from_pile("Masquerade")

    def test_suitable(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.other.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.third.piles[Piles.HAND].set()
        self.assertEqual(suitable_players(self.g), [self.plr, self.other])

    def test_plr_to_left(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.other.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.third.piles[Piles.HAND].set()
        players = suitable_players(self.g)
        self.assertEqual(plr_to_left(players, self.plr), self.other)
        self.assertEqual(plr_to_left(players, self.other), self.plr)

    def test_play(self) -> None:
        """Play a masquerade"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.other.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.third.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["select silver", "finish"]
        self.other.test_input = ["select duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.other.piles[Piles.HAND])
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_play_with_trash(self) -> None:
        """Play a masquerade and trash after"""
        tsize = self.g.trash_pile.size()
        self.other.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.third.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["select gold", "trash silver"]
        self.other.test_input = ["select gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 - 1)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
