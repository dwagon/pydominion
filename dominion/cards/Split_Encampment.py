#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Encampment"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Encampment(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+2 Cards; +2 Actions; You may reveal a Gold or Plunder
            from your hand. If you do not, set this aside, and return it to the
            Supply at the start of Clean-up."""
        self.name = "Encampment"
        self.cards = 2
        self.actions = 2
        self.cost = 2
        self._discard = False
        self.pile = "Encampment"

    def special(self, game, player):
        gold = player.piles[Piles.HAND]["Gold"]
        plunder = player.piles[Piles.HAND]["Plunder"]
        if gold or plunder:
            self._discard = False
            choice = player.plr_choose_options(
                "Reveal Gold or Plunder to avoid returning this card",
                ("Reveal card", True),
                ("Return Encampment", False),
            )
            if choice:
                if gold:
                    player.reveal_card(gold)
                if plunder:
                    player.reveal_card(plunder)
            else:
                self._discard = True
        else:
            self._discard = True

    def hook_cleanup(self, game, player):
        if self._discard:
            for card in player.piles[Piles.PLAYED]:
                if card == self:
                    player.output("Returning Encampment to Supply")
                    player.move_card(self, Piles.CARDPILE)
                    self._discard = False
                    return


###############################################################################
class TestEncampment(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Encampment"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Encampment")

    def test_play_reveal(self):
        """Play an Encampment and reveal a Gold"""
        self.plr.piles[Piles.HAND].set("Gold")
        hndsz = self.plr.piles[Piles.HAND].size()
        acts = self.plr.actions.get()
        self.plr.test_input = ["Reveal card"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz + 2)
        self.assertEqual(self.plr.actions.get(), acts + 2 - 1)
        self.assertEqual(self.card._discard, False)
        self.plr.cleanup_phase()
        self.assertEqual(len(self.g.card_piles["Encampment"]), 9)

    def test_play_return(self):
        """Play an Encampment and don't have anything to return"""
        self.plr.piles[Piles.DISCARD].set(
            "Copper", "Copper", "Copper", "Estate", "Estate"
        )
        self.plr.piles[Piles.HAND].set("Silver")
        hand_size = self.plr.piles[Piles.HAND].size()
        acts = self.plr.actions.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hand_size + 2)
        self.assertEqual(self.plr.actions.get(), acts + 2 - 1)
        self.assertEqual(self.card._discard, True)
        self.plr.cleanup_phase()
        self.assertEqual(len(self.g.card_piles["Encampment"]), 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
