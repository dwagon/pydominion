#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Tribute """

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Tribute(Card.Card):
    """Tribute"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """ The player to your left reveals then discards the top
            2 cards of his deck. For each differently named card revealed,
            if is an Action card, +2 actions; treasure card, +2 coin;
            victory card, +2 cards """
        self.name = "Tribute"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Tribute Special"""
        victim = game.player_to_left(player)
        cards = []
        for _ in range(2):
            try:
                card = victim.next_card()
            except NoCardException:
                continue
            victim.reveal_card(card)
            cards.append(card)
        card_name = None
        for card in cards:
            player.output(f"Looking at {card} from {victim.name}")
            victim.output(f"{player.name}'s Tribute discarded {card}")
            victim.add_card(card, "discard")
            if card.name == card_name:
                player.output("Duplicate - no extra")
                continue
            card_name = card.name
            if card.isAction():
                player.output("Gained two actions")
                player.add_actions(2)
            elif card.isTreasure():
                player.output("Gained two coin")
                player.coins.add(2)
            elif card.isVictory():
                player.output("Gained two cards")
                player.pickup_cards(2)


###############################################################################
class TestTribute(unittest.TestCase):
    """Test Tribute"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Tribute"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Tribute")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a tribute"""
        self.victim.piles[Piles.DECK].set("Copper", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)

    def test_same(self) -> None:
        """Victim has the same cards for Tribute"""
        self.victim.piles[Piles.DECK].set("Tribute", "Tribute")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
