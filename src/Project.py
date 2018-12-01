from Card import Card


class Project(Card):
    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)
        self.cardtype = 'project'

# EOF
