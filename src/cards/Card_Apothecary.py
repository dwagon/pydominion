from Card import Card


class Card_Apothecary(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+1 card, +1 action, Take coppers and potions out of top 4 of deck"
        self.name = 'Apothecary'
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.potcost = 1

    def special(self, player, game):
        """ Reveal the top 4 cards of your deck. Put the revealed
            Coppers and Potions into your gand. Put the other cards
            back on top of your deck in any order """
        unput = []
        for i in range(4):
            c = player.nextCard()
            if c.name in ('Copper', 'Potion'):
                print "Putting %s in hand " % c.name
                player.addCard(c, 'hand')
            else:
                unput.append(c)
        for c in unput:
            print "Putting %s back in deck" % c.name
            player.addCard(c, 'deck')


#EOF
