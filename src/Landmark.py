class Landmark(object):
    def __init__(self):
        self.image = None
        self.cost = 0
        self.desc = 'TODO'

    def hook_endTurn(self, game, player):   # pragma: no cover
        return

    def hook_preBuy(self, game, player):    # pragma: no cover
        return

    def hook_gainCard(self, game, player, card):    # pragma: no cover
        return

# EOF
