#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Clerk"""

import unittest

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Clerk(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.REACTION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+$2; Each other player with 5 or more cards in hand puts one onto their deck.
        At the start of your turn, you may play this from your hand."""
        self.name = "Clerk"
        self.cost = 4
        self.coin = 2

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Each other player with 5 or more cards in hand puts one onto their deck."""
        """ TODO - play it free at the start of the turn """
        for victim in player.attack_victims():
            hand_size = len(victim.piles[Piles.HAND])
            if hand_size >= 5:
                self.attack(player, victim)
            else:
                player.output(f"{victim.name} only has {hand_size} cards")

    def attack(self, attacker: "Player.Player", victim: "Player.Player") -> None:
        """{victim} puts one onto their deck"""
        victim.output(f"Under attack by {attacker.name}'s Clerk")
        card = victim.card_sel(
            num=1,
            prompt="Clerk forces you to put a card back onto your deck",
            force=True,
            select_from=Piles.HAND,
        )[0]
        victim.move_card(card, Piles.DECK)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(1)


###############################################################################
class TestClerk(unittest.TestCase):
    """Test Clerk"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Clerk"])
        self.g.start_game()
        self.player, self.victim = self.g.player_list()
        self.clerk = self.g.get_card_from_pile("Clerk")
        self.player.add_card(self.clerk, Piles.HAND)

    def test_play(self) -> None:
        coins = self.player.coins.get()
        self.victim.piles[Piles.HAND].set("Copper", "Copper", "Copper", "Copper", "Estate", "Duchy")
        self.victim.test_input = ["Select Duchy", "Finish"]
        self.player.play_card(self.clerk)
        self.assertEqual(self.player.coins.get(), coins + 2)
        self.assertNotIn("Duchy", self.victim.piles[Piles.HAND])
        self.assertIn("Duchy", self.victim.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
