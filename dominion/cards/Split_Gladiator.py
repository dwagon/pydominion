#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Gladiator"""
import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Gladiator(Card.Card):
    """Gladiator"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+2 Coin; Reveal a card from your hand. The player to your left may reveal a copy from their hand.
        If they do not, +1 Coin and trash a Gladiator from the Supply."""
        self.name = "Gladiator"
        self.cost = 3
        self.coin = 2
        self.numcards = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if not player.piles[Piles.HAND]:
            return
        if my_card := player.card_sel(
            num=1,
            force=True,
            prompt="Select a card from your hand that the player to your left doesn't have",
        ):
            player.reveal_card(my_card[0])
            lefty = game.player_to_left(player)
            if lefty_card := lefty.piles[Piles.HAND][my_card[0].name]:
                player.output(f"{lefty} has a {my_card[0]}")
                lefty.reveal_card(lefty_card)
            else:
                player.output(f"{lefty} doesn't have a {my_card[0]}")
                player.coins.add(1)
                if game.card_piles["Gladiator"].top_card() == "Gladiator":
                    card = game.card_piles["Gladiator"].get_top_card()
                    assert card is not None
                    player.output("Trashing Gladiator from Supply")
                    player.trash_card(card)


###############################################################################
class TestGladiator(unittest.TestCase):
    """Test Gladiator"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Gladiator", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Gladiator")

    def test_play_not_have(self) -> None:
        """Play a Gladiator - something the other player doesn't have"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat"]
        num_gladiators = len(self.g.card_piles["Gladiator"])
        self.plr.play_card(self.card)
        self.assertIn("Gladiator", self.g.trash_pile)
        self.assertEqual(len(self.g.card_piles["Gladiator"]), num_gladiators - 1)
        self.assertEqual(self.plr.coins.get(), 3)

    def test_play_has(self) -> None:
        """Play a Gladiator - something the other player has"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.vic.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gladiator", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
