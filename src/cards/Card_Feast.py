from Card import Card


class Card_Feast(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash this card, Gain a card costing up to 5"
        self.name = 'Feast'
        self.cost = 4

    def special(self, game, player):
        """ Trash this card. Gain a card costing up to 5 """
        if self.trashCard(player):
            self.selectNewCard(game, player)

    def selectNewCard(self, game, player):
        print "Feast: Gain a card costing up to 5"
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        purchasable = game.cardsUnder(5)
        index = 1
        for p in purchasable:
            selector = "%d" % index
            toprint = 'Get %s (%d gold)' % (p.name, p.cost)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1

        o = player.userInput(options, "What card do you wish?")
        player.gainCard(o['card'])
        print "Took %s" % o['card'].name
        return

    def trashCard(self, player):
        options = [
            {'selector': '0', 'print': "Don't trash this card", 'trash': False},
            {'selector': '1', 'print': "Trash this card", 'trash': True}
            ]
        o = player.userInput(options, "Trash this card?")
        if o['trash']:
            player.trashCard(self)

#EOF
