#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Venture(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.desc = "+1 coin, get next treasure from deck"
        self.base = Card.CardExpansion.PROSPERITY
        self.name = "Venture"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """When you play this, reveal cards from your deck until
        you reveal a Treasure. Discard the other cards. Play that
        Treasure"""
        max_cards = player.count_cards()
        count = 0
        while True:
            count += 1
            if count >= max_cards:
                player.output("No suitable cards")
                break
            try:
                card = player.pickup_card(verbose=False)
            except NoCardException:
                break
            player.reveal_card(card)
            if card.isTreasure():
                player.output(f"Picked up {card} from Venture")
                player.play_card(card)
                break
            player.output(f"Picked up and discarded {card}")
            player.coins.add(card.coin)  # Compensate for not keeping card
            player.discard_card(card)


###############################################################################
class TestVenture(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Venture"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Venture")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Venture"""
        self.plr.piles[Piles.DECK].set("Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)  # Gold
        for c in self.plr.piles[Piles.PLAYED]:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail("Didn't play the gold")
        self.assertTrue(self.plr.piles[Piles.DECK].is_empty())

    def test_discard(self) -> None:
        """Make sure we discard non-treasures"""
        self.plr.piles[Piles.DECK].set("Gold", "Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)  # Gold
        for c in self.plr.piles[Piles.PLAYED]:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail("Didn't play the gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            if c.name != "Estate":  # pragma: no cover
                self.fail("Didn't discard the non-treasure")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
