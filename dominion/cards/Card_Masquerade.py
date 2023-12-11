#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Masquerade"""
import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Masquerade(Card.Card):
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
        xfer = {}
        for plr in game.player_list():
            if len(plr.piles[Piles.HAND]):
                xfer[plr] = self.pick_card_to_xfer(game, plr)
        for plr in list(xfer.keys()):
            new_player = game.player_to_left(plr)
            new_card = xfer[plr]
            new_card.player = new_player
            new_player.output(f"You received a {new_card} from {plr}")
            new_player.add_card(new_card, Piles.HAND)
        player.plr_trash_card()

    def pick_card_to_xfer(self, game: Game.Game, plr: Player.Player) -> Card.Card:
        leftplr = game.player_to_left(plr).name
        if cards := plr.card_sel(
            prompt=f"Which card to give to {leftplr}?", num=1, force=True
        ):
            card = cards[0]
            plr.piles[Piles.HAND].remove(card)
            plr.output(f"Gave {card} to {leftplr}")
            return card


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    c = player.pick_to_discard(1, keepvic=True)
    return c


###############################################################################
class TestMasquerade(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Masquerade"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Masquerade")

    def test_play(self) -> None:
        """Play a masquerade"""
        tsize = self.g.trash_pile.size()
        self.other.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["select silver", "finish"]
        self.other.test_input = ["select gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.other.piles[Piles.HAND])
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_play_with_trash(self) -> None:
        """Play a masquerade and trash after"""
        tsize = self.g.trash_pile.size()
        self.other.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
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
