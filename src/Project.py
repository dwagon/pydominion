from Card import Card


class Project(Card):
    def __init__(self, *args, **kwargs):
        Card.__init__(self, *args, **kwargs)
        self.cardtype = 'project'

# EOF
