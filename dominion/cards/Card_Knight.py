#!/usr/bin/env python

import random
import unittest
from dominion import Card, CardPile, Game


###############################################################################
class Card_Knight(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Knights"
        self.base = Card.CardExpansion.DARKAGES

    def setup(self, game):
        game.cardpiles["Knights"] = KnightCardPile(game)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class KnightCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("KnightCard", game.paths["cards"], "Card_")
        super().__init__(
            cardname="Knight",
            klass=None,
            game=game,
        )

    def __getattr__(self, name):
        return getattr(self._cards[0], name)

    def init_cards(self):
        self._cards = [_() for _ in self.mapping.values()]
        random.shuffle(self._cards)


###############################################################################
class KnightCard(Card.Card):
    def __init__(self):
        self.name = "Undef Knight"
        super().__init__()

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
                victim.output("%s's %s discarded your %s" % (player.name, self.name, crd.name))
                victim.discard_card(crd)
        if not cards:
            return
        player.output("Looking at %s" % ", ".join([x.name for x in cards]))

        trash = victim.plr_trash_card(
            cardsrc=cards,
            force=True,
            prompt="%s's %s trashes one of your cards" % (player.name, self.name),
        )
        to_trash = trash[0]
        player.output("%s trashed a %s" % (victim.name, to_trash.name))

        if to_trash.isKnight():
            player.output("%s trashed a knight: %s - trashing your %s" % (victim.name, to_trash.name, self.name))
            player.trash_card(self)

        for crd in cards:
            if crd != to_trash:
                victim.output("%s's %s discarded your %s" % (player.name, self.name, crd.name))
                victim.discard_card(crd)


###############################################################################
class Test_Knight(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Knights"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = None
        self.card = self.g["Knights"].remove()

        # Makes testing harder due to card actions
        while self.card.name in ("Dame Anna", "Dame Natalie", "Sir Michael"):
            self.card = self.g["Knights"].remove()

        self.plr.hand.set("Silver", "Gold")
        self.plr.add_card(self.card, "hand")

    def test_playcard_nosuitable(self):
        """Play a knight woth no suitable cards"""
        self.vic.deck.set("Copper", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.discardpile.size(), 2)

    def test_playcard_one_suitable(self):
        """Play a knight with one suitable card"""
        self.vic.deck.set("Copper", "Duchy")
        self.vic.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.discardpile.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
