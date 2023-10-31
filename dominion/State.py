from dominion import Card


###############################################################################
class State(Card.Card):
    def __init__(self) -> None:
        super().__init__()
        self.cardtype = Card.CardType.STATE
        self.unique_state = False


# EOF
