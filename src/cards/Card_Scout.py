from Card import Card


class Card_Scout(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 action, Adjust top 4 cards of deck"
        self.name = 'Scout'
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Reveal the top 4 cards of your deck. Put the revealed
            victory cards into your hand. Put the other cards on top
            of your deck in any order """
        #TODO: Currently you can't order the cards you return
        cards = []
        for i in range(4):
            c = player.nextCard()
            if c.isVictory():
                player.addCard(c, 'hand')
                player.output("Adding %s to hand" % c.name)
            else:
                cards.append(c)
        for c in cards:
            player.output("Putting %s back on deck" % c.name)
            player.addCard(c, 'deck')
#EOF
