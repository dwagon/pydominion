"""http://wiki.dominionstrategy.com/index.php/Trait"""

from dominion import Card, Game


###############################################################################
class Trait(Card.Card):
    """Class representing traits - mostly just card code"""

    ###########################################################################
    def isTraitCard(self, game: "Game.Game", card: Card.Card) -> bool:
        """Return if this card is the trait"""
        if card.pile not in game.card_piles:
            return False
        return game.card_piles[card.pile].trait == self.name

    ###########################################################################
    def __repr__(self) -> str:
        return f"Trait {self.name}"


# EOF
