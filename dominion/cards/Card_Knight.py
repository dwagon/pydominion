#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Knight"""

import random
import unittest
from dominion import Card, CardPile, Game, Piles


###############################################################################
class Card_Knight(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Knights"
        self.base = Card.CardExpansion.DARKAGES

    @classmethod
    def cardpile_setup(cls, game):
        """Setup"""
        card_pile = KnightCardPile(game)
        return card_pile


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class KnightCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("KnightCard", game.paths["cards"], "Card_")
        for name, class_ in self.mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        self.cards = [_() for _ in self.mapping.values()]
        random.shuffle(self.cards)

    def isVictory(self):
        """Knight Pile is not considered a Victory pile"""
        return False


###############################################################################
class KnightCard(Card.Card):
    def __init__(self):
        self.name = "Undef Knight"
        super().__init__()
        self.pile = "Knights"

    def knight_special(self, game, player):
        """Each other player reveals the top 2 cards of his deck,
        trashes one of them costing from 3 to 6 and discards the
        rest. If a knight is trashed by this, trash this card"""
        for pl in player.attack_victims():
            self.knight_attack(game, player, pl)

    def knight_attack(self, game, player, victim):
        cards = []
        for _ in range(2):
            crd = victim.next_card()
            victim.reveal_card(crd)
            if crd.cost in (3, 4, 5, 6):
                cards.append(crd)
            else:
                victim.output(f"{player.name}'s {self} discarded your {crd}")
                victim.discard_card(crd)
        if not cards:
            return
        player.output("Looking at %s" % ", ".join([_.name for _ in cards]))

        trash = victim.plr_trash_card(
            cardsrc=cards,
            force=True,
            prompt=f"{player.name}'s {self} trashes one of your cards",
        )
        to_trash = trash[0]
        player.output(f"{victim.name} trashed a {to_trash}")

        if to_trash.isKnight():
            player.output(
                f"{victim.name} trashed a knight: {to_trash} - trashing your {self}"
            )
            player.trash_card(self)

        for crd in cards:
            if crd != to_trash:
                victim.output(f"{player.name}'s {self} discarded your {crd}")
                victim.discard_card(crd)


###############################################################################
class TestKnight(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Knights"])
        self.g.start_game()
        self.player, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Knights", "Dame Josephine")

        self.player.piles[Piles.HAND].set("Silver", "Gold")
        self.player.add_card(self.card, Piles.HAND)

    def test_play_card_no_suitable(self):
        """Play a knight with no suitable cards"""
        self.victim.piles[Piles.DECK].set("Copper", "Copper")
        self.player.play_card(self.card)
        self.assertEqual(len(self.victim.piles[Piles.DISCARD]), 2)

    def test_play_card_one_suitable(self):
        """Play a knight with one suitable card"""
        self.victim.piles[Piles.DECK].set("Copper", "Duchy")
        self.victim.test_input = ["Duchy"]
        self.player.play_card(self.card)
        self.assertEqual(len(self.victim.piles[Piles.DISCARD]), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
