#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Shaman"""
import random
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Shaman(Card.Card):
    """Shaman"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Action; +$1; You may trash a card from your hand.
            In games using this, at the start of your turn, gain a card from the trash costing up to $6."""
        self.name = "Shaman"
        self.cost = 2
        self.actions = 1
        self.coin = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may trash a card from your hand."""
        player.plr_trash_card(num=1)

    def hook_start_every_turn(self, game: Game.Game, player: Player.Player) -> None:
        """In games using this, at the start of your turn, gain a card from the trash costing up to $6."""
        if game.trash_pile.is_empty():
            return
        options = []
        for card in game.trash_pile:
            if player.card_cost(card) <= 6:
                options.append((f"Get {card} from trash", card))
        if not options:
            player.output("No suitable cards in trash")
            return
        from_trash = player.plr_choose_options("Shaman: Pick a card to gain from the trash", *options)
        player.move_card(from_trash, Piles.DISCARD)
        player.output(f"Gained {from_trash} from the trash pile")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    """Try and get a treasure"""
    for _, card in args:
        if card.isTreasure():
            return card
    return random.choice(args)[1]


###############################################################################
class TestShaman(unittest.TestCase):
    """Test Shaman"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Shaman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Shaman")

    def test_play(self) -> None:
        """Play a Shaman"""
        self.plr.piles[Piles.HAND].set("Copper", "Duchy", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        actions = self.plr.actions.get()
        self.plr.test_input = ["Trash Duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.assertEqual(self.plr.actions.get(), actions)  # +1 for the Shaman, -1 for playing the Shaman
        self.assertIn("Duchy", self.g.trash_pile)

    def test_start_turn(self) -> None:
        """Start of a turn"""
        self.g.trash_pile.set("Gold")
        self.plr.test_input = ["Get Gold"]
        self.plr.start_turn()
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
