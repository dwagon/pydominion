#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Mint"""
import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Mint(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.name = "Mint"
        self.cost = 5

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """You may reveal a Treasure card from your hand. Gain a copy of it.
            When you buy this, trash all Treasures you have in play."""
        return "You may reveal a Treasure card from your hand. Gain a copy of it."

    def special(self, game, player):
        treasures = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treasures:
            player.output("No treasures to reveal")
            return
        to_get = player.card_sel(
            num=1, cardsrc=treasures, prompt="Reveal a treasure to gain a copy of"
        )
        player.reveal_card(to_get[0])
        if to_get:
            player.output(f"Gained a {to_get[0]} from the Mint")
            player.gain_card(to_get[0].name)

    def hook_buy_this_card(self, game, player):
        """Trash all Treasures you have in play"""
        to_trash = [c for c in player.piles[Piles.PLAYED] if c.isTreasure()]
        for c in to_trash:
            player.output(f"Mint trashing {c.name}")
            player.trash_card(c)


###############################################################################
class TestMint(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mint", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mint"].remove()

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Duchy", "Gold", "Silver", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gold", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])

    def test_buy(self):
        tsize = self.g.trashpile.size()
        self.plr.coins.set(5)
        self.plr.piles[Piles.HAND].set("Gold", "Estate")
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Estate", "Moat")
        self.plr.buy_card("Mint")
        self.assertEqual(self.g.trashpile.size(), tsize + 2)
        self.assertIn("Copper", self.g.trashpile)
        self.assertIn("Silver", self.g.trashpile)
        self.assertNotIn("Gold", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
