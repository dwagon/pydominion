from Card import Card


class Card_Vineyard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "num action cards / 3 VP"
        self.name = 'Vineyard'
        self.playable = False
        self.cost = 0
        self.potcost = 1

    def special_score(self, game, player):
        """ Worth 1VP for every 3 action cards in your deck rounded down """
        score = 0
        for c in player.discardpile + player.hand + player.deck:
            if c.isAction():
                score += 1
        return score / 3

#EOF
