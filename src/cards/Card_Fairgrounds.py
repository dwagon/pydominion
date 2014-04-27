from Card import Card


class Card_Fairgrounds(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "2VP / 5 card types"
        self.name = 'Fairgrounds'
        self.playable = False
        self.cost = 6

    def special_score(self, game, player):
        """ Worth 2VP for every 5 differently named cards in your deck (round down)"""

        numtypes = len(set(player.discardpile + player.hand + player.deck))
        return 2 * int(numtypes / 5)

#EOF
