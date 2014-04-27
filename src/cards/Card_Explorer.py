from Card import Card


class Card_Explorer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Reveal a provice to gain gold else gain silver"
        self.name = 'Explorer'
        self.cost = 5

    def special(self, game, player):
        """ You may reveal a Province card from you hand. If you
            do, gain a Gold card, putting it into your hand. Otherise,
            gain a Silver card, putting it into your hand """
        if player.inHand('province'):
            player.gainCard('Gold', destination='hand')
        else:
            player.gainCard('Silver', destination='hand')

#EOF
