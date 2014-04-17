from Card import Card


class Card_Remodel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a card and gain one costing 2 more"
        self.name = 'Remodel'
        self.image = 'images/remodel.jpg'
        self.cost = 2

    def special(self, game, player):
        """ Trash c card from your hand. Gain a card costing up to
            2 more than the trashed card """
        cost = self.trashCard(game, player)
        if cost:
            self.gainCard(cost + 2, game, player)

    def gainCard(self, cost, game, player):
        print "Gain a card costing up to %d" % cost
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        purchasable = game.cardsUnder(cost)
        index = 1
        for p in purchasable:
            selector = "%d" % index
            toprint = 'Get %s (%d gold) %s' % (p.name, p.cost, p.desc)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1

        o = player.userInput(options, "What card do you wish?")
        if o:
            player.addCard(o['card'].remove())

    def trashCard(self, game, player):
        print "Trash a card"
        options = [{'selector': '0', 'print': 'Trash nothing', 'card': None}]
        index = 1
        for c in player.hand:
            sel = "%d" % index
            pr = "Trash %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Trash which card?")
        if not o['card']:
            return
        trash = o['card']
        player.trashCard(trash)
        return trash.cost

#EOF
