from Card import Card


class Card_Masquerade(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+2 cards. Every player passes a card on, and you trash a card"
        self.name = 'Masquerade'
        self.cards = 2
        self.cost = 3

    def special(self, player, game):
        """ Each player passes a card from his hand to the left at
            once. Then you may trash a card from your hand"""

        xfer = {}
        for plr in game.players:
            xfer[plr] = self.pickCardToXfer(plr, game)
        for plr in xfer.keys():
            newplr = game.playerToLeft(plr)
            newcrd = xfer[plr]
            newplr.output("You gained a %s from %s" % (newcrd.name, plr.name))
            newplr.addCard(newcrd, 'hand')
        player.plrTrashCard()

    def pickCardToXfer(self, plr, game):
        index = 1
        options = []
        for c in plr.hand:
            sel = "%d" % index
            pr = "Select %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = plr.userInput(options, "Which card to give to %s?" % game.playerToLeft(plr).name)
        plr.hand.remove(o['card'])
        return o['card']

#EOF
