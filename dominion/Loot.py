""" https://wiki.dominionstrategy.com/index.php/Loot"""
import random
from dominion import Card, CardPile, Keys, Piles


###############################################################################
class LootPile(CardPile.CardPile):
    def __init__(self, game) -> None:
        self.mapping = game.get_card_classes("Loot", game.paths[Keys.LOOT], "Loot_")
        for name, class_ in self.mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards: int = 0, card_class=None) -> None:
        """2 of each loot card"""
        for loot_card in self.mapping.values():
            for _ in range(2):
                card = loot_card()
                card.location = Piles.CARDPILE
                self.cards.append(card)
        random.shuffle(self.cards)


###############################################################################
class Loot(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.purchasable = False


# EOF
