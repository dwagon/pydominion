

###############################################################################
class ProjectPile(object):
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.project = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.project, name)

    ###########################################################################
    def __repr__(self):
        return self.name

# EOF
