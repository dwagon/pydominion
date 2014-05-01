from Card import Card


class Card_Baron(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 Buy, discard an estate gain +4 Gold, else gain estate"
        self.name = 'Baron'
        self.cost = 4
        self.buys = 1

    def special(self, game, player):
        """ You may discard an Estate card. If you do +4 GP. Otherwise,
            gain an estate card """

        hasEstate = player.inHand('Estate')

        if hasEstate:
            options = [
                {'selector': '0', 'print': "Don't trash an Estate - Gain Estate", 'trash': False},
                {'selector': '1', 'print': "Trash an Estate - Gain +4 Gold", 'trash': True}]
            o = player.userInput(options, "Trash Estate")
            if o['trash']:
                player.output("Trashed %s" % hasEstate.cardname)
                player.trashCard(hasEstate)
                player.t['gold'] += 4
                return
        print("Gained an Estate")
        player.addCard(game['Estate'].remove())

#EOF
