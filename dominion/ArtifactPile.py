###############################################################################
class ArtifactPile:
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.artif = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.artif, name)

    ###########################################################################
    def __repr__(self):
        return self.name


# EOF
