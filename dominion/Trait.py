"""http://wiki.dominionstrategy.com/index.php/Trait"""

from dominion import Game, Player, Card


###############################################################################
class Trait(Card.Card):
    """Class representing traits - mostly just card code"""

    def __init__(self):
        self.card_pile = ""
        super().__init__()

    ###########################################################################
    def isTraitCard(self, game: "Game.Game", card: Card.Card) -> bool:
        """Return if this card is the trait"""
        if card.pile not in game.card_piles:
            return False
        return game.card_piles[card.pile].trait == self.name

    ###########################################################################
    def hook_all_card_description(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> str:
        if self.isTraitCard(game, card):
            return f"[Trait: {self.name}]"
        return ""

    ###########################################################################
    def __repr__(self) -> str:  # pragma: no coverage
        return f"Trait {self.name}"


# EOF
