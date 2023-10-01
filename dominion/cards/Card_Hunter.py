#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Hunter"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Hunter(Card.Card):
    """Hunter"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.desc = """ +1 Action; Reveal the top 3 cards of your deck. 
        From those cards, put an Action, a Treasure, and a Victory card into your hand. Discard the rest."""
        self.name = "Hunter"
        self.actions = 1
        self.cost = 5

    def hunter_special(self, all_cards, player, typed_cards, card_description):
        """Abstract out repeat code"""
        if typed_cards:
            if len(typed_cards) > 1:
                card = player.card_sel(
                    num=1,
                    force=True,
                    prompt=f"Pick {card_description} to put in your hand",
                    cardsrc=typed_cards,
                )[0]
            else:
                card = typed_cards[0]
            all_cards.remove(card)
            player.output(f"Putting {card} into hand")
            player.add_card(card, Piles.HAND)

    def special(self, game, player):
        cards = [player.next_card() for _ in range(3)]
        for card in cards:
            player.reveal_card(card)
        self.hunter_special(
            cards, player, [_ for _ in cards if _.isAction()], "an action"
        )
        self.hunter_special(
            cards, player, [_ for _ in cards if _.isTreasure()], "a treasure"
        )
        self.hunter_special(
            cards, player, [_ for _ in cards if _.isVictory()], "a victory"
        )
        for card in cards:
            player.output(f"Discarding {card}")
            player.discard_card(card)


###############################################################################
class Test_Hunter(unittest.TestCase):
    """Test Hunter"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hunter", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Hunter")

    def test_play(self):
        """Play a hunter"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
