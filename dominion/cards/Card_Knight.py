#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Knight"""

import random
import unittest
from dominion import Card, CardPile, Game, Piles, Player, NoCardException


###############################################################################
class Card_Knight(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.name = "Knights"
        self.base = Card.CardExpansion.DARKAGES

    @classmethod
    def cardpile_setup(cls, game: Game.Game):
        """Setup"""
        return KnightCardPile(game)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class KnightCardPile(CardPile.CardPile):
    def __init__(self, game: Game.Game) -> None:
        self.mapping = game.get_card_classes("KnightCard", game.paths["cards"], "Card_")
        for name, class_ in self.mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards: int = 0, card_class=None) -> None:
        self.cards = [_() for _ in self.mapping.values()]
        random.shuffle(self.cards)

    def isVictory(self) -> bool:
        """Knight Pile is not considered a Victory pile"""
        return False


###############################################################################
class KnightCard(Card.Card):
    def __init__(self) -> None:
        self.name = "Undef Knight"
        super().__init__()
        self.pile = "Knights"

    def knight_special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other player reveals the top 2 cards of his deck,
        trashes one of them costing from 3 to 6 and discards the
        rest. If a knight is trashed by this, trash this card"""
        for pl in player.attack_victims():
            self.knight_attack(game, player, pl)

    def knight_attack(
        self, game: Game.Game, player: Player.Player, victim: Player.Player
    ) -> None:
        cards: list[Card.Card] = []
        for _ in range(2):
            try:
                card = victim.next_card()
            except NoCardException:
                continue

            victim.reveal_card(card)

            if card.cost in (3, 4, 5, 6):
                cards.append(card)
            else:
                victim.output(f"{player.name}'s {self} discarded your {card}")
                victim.discard_card(card)
        if not cards:
            return
        player.output(f'Looking at {", ".join([_.name for _ in cards])}')

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

        for card in cards:
            if card != to_trash:
                victim.output(f"{player.name}'s {self} discarded your {card}")
                victim.discard_card(card)


###############################################################################
class TestKnight(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Knights"])
        self.g.start_game()
        self.player, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Knights", "Dame Josephine")

        self.player.piles[Piles.HAND].set("Silver", "Gold")
        self.player.add_card(self.card, Piles.HAND)

    def test_play_card_no_suitable(self) -> None:
        """Play a knight with no suitable cards"""
        self.victim.piles[Piles.DECK].set("Copper", "Copper")
        self.player.play_card(self.card)
        self.assertEqual(len(self.victim.piles[Piles.DISCARD]), 2)

    def test_play_card_one_suitable(self) -> None:
        """Play a knight with one suitable card"""
        self.victim.piles[Piles.DECK].set("Copper", "Duchy")
        self.victim.test_input = ["Duchy"]
        self.player.play_card(self.card)
        self.assertEqual(len(self.victim.piles[Piles.DISCARD]), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
