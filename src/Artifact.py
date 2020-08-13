import Card


class Artifact(Card.Card):
    def __init__(self, *args, **kwargs):
        super(Artifact, self).__init__(*args, **kwargs)
        self.cardtype = Card.TYPE_ARTIFACT

# EOF
