from dominion import Card


class Artifact(Card.Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cardtype = Card.TYPE_ARTIFACT


# EOF
