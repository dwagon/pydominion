#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Sea_Witch"""

import unittest

from dominion import Card, Game, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_SeaWitch(Card.Card):
    """Sea Witch"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+2 Cards; Each other player gains a Curse.
            At the start of your next turn, +2 Cards, then discard 2 cards."""
        self.name = "Sea Witch"
        self.required_cards = ["Curse"]
        self.cards = 2
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for victim in player.attack_victims():
            try:
                victim.gain_card("Curse")
                victim.output(f"{player}'s Sea Witch cursed you")
                player.output(f"{victim} got cursed")
            except NoCardException:
                player.output("No more Curses")

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        """+2 card, discard 2"""
        player.pickup_cards(2)
        player.plr_discard_cards(num=2, force=True)
        return {}


###############################################################################
class TestSeaWitch(unittest.TestCase):
    """Test Sea Witch"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Sea Witch"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Sea Witch")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a sea witch"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Discard Estate", "Discard Duchy", "Finish"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2 - 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
