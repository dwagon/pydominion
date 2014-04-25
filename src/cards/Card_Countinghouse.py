from Card import Card


class Card_Countinghouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Pull coppers out of discard"
        self.name = 'Counting House'
        self.cost = 5

    def special(self, game, player):
        """ Look through the discard pile, reveal any number of
            copper cards from it, and put them into your hand """
        count = 0
        for c in player.discardpile:
            if c.cardname == 'copper':
                player.addCard(c, 'hand')
                count += 1
        player.output("Picked up %d coppers" % count)

#EOF
