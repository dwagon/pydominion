#!/usr/bin/env python

import unittest
from dominion import Card, Game, CardPile


###############################################################################
class Card_Odysseys(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Odysseys"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]
        self.numcards = 1

    @classmethod
    def cardpile_setup(cls, game):
        return OdysseyCardPile(game)


###############################################################################
class OdysseyCardPile(CardPile.CardPile):
    def __init__(self, game, pile_size=12):
        self.mapping = game.getSetCardClasses(
            "Odysseys", game.cardpath, "dominions/cards", "Card_"
        )
        super().__init__(
            cardname="Odysseys", klass=None, game=game, pile_size=pile_size
        )

    def init_cards(self):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Odyssey_Old_Map import Card_Old_Map
        from dominion.cards.Odyssey_Voyage import Card_Voyage
        from dominion.cards.Odyssey_Sunken_Treasure import Card_Sunken_Treasure
        from dominion.cards.Odyssey_Distant_Shore import Card_Distant_Shore

        self._cards = []
        for crd in (
            Card_Old_Map,
            Card_Voyage,
            Card_Sunken_Treasure,
            Card_Distant_Shore,
        ):
            for _ in range(4):
                self._cards.insert(0, crd())


###############################################################################
class Test_Odysseys(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_augurs(self):
        card = self.g["Odysseys"].remove()
        self.assertEqual(len(self.g["Odysseys"]), 15)
        self.assertEqual(card.name, "Old Map")
        card = self.g["Odysseys"].remove()
        card = self.g["Odysseys"].remove()
        card = self.g["Odysseys"].remove()
        card = self.g["Odysseys"].remove()
        self.assertEqual(card.name, "Voyage")
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
