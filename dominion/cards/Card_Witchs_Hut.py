#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Witch%27s_Hut"""

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Witchs_Hut(Card.Card):
    """Witchs Hut"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+4 Cards; Discard 2 cards, revealed.
            If they're both Actions, each other player gains a Curse."""
        self.name = "Witch's Hut"
        self.cost = 5
        self.required_cards = ["Curse"]
        self.cards = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        cards = player.plr_discard_cards(2)
        num_acts = 0
        for card in cards:
            player.reveal_card(card)
            if card.isAction():
                num_acts += 1
        if num_acts == 2:
            for plr in player.attack_victims():
                plr.output(f"{player.name}s Witch's Hut cursed you")
                plr.gain_card("Curse")


###############################################################################
class Test_Witchs_Hut(unittest.TestCase):
    """Test Witch's Hut"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, initcards=["Witch's Hut", "Moat", "Chapel"]
        )
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Witch's Hut")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_curse(self) -> None:
        """Play the Witchs Hut and hand out a curse"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Moat", "Chapel")
        self.plr.test_input = ["Discard Moat", "Discard Chapel", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.oth.piles[Piles.DISCARD])

    def test_play_no_curse(self) -> None:
        """Play the Witch's Hut and don't curse"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Moat", "Chapel")
        self.plr.test_input = ["Discard Copper", "Discard Chapel", "Finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Curse", self.oth.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
