#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Pillage"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Pillage(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Trash this. Each other player with 5 or more cards in hand
        reveals their hand and discards a card that you choose. Gain 2 Spoils
        from the Spoils pile."""
        self.name = "Pillage"
        self.required_cards = ["Spoils"]
        self.cost = 5

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.trash_card(self)
        for plr in player.attack_victims():
            if plr.piles[Piles.HAND].size() < 5:
                player.output(f"Player {plr} has too small a hand size")
                continue
            self.pick_a_card(plr, player)
        for _ in range(2):
            try:
                player.gain_card("Spoils")
            except NoCardException:
                player.output("No more Spoils")
                break

    ###########################################################################
    def pick_a_card(self, victim: Player.Player, player: Player.Player) -> None:
        """pillage a players hand"""
        for card in victim.piles[Piles.HAND]:
            victim.reveal_card(card)
        if cards := player.card_sel(
            cardsrc=victim.piles[Piles.HAND],
            prompt=f"Which card to discard from {victim}",
        ):
            card = cards[0]
            victim.discard_card(card)
            victim.output(f"{player} pillaged your {card}")


###############################################################################
class TestPillage(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Pillage"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Pillage")

    def test_play(self) -> None:
        """Play the Pillage"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["copper"]
        self.victim.piles[Piles.HAND].set("Copper", "Estate", "Duchy", "Gold", "Silver", "Province")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Spoils")
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Copper")

    def test_short_hand(self) -> None:
        """Play the Pillage with the victim having a small hand"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["copper"]
        self.victim.piles[Piles.HAND].set("Copper", "Estate", "Duchy", "Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Spoils")
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 4)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
