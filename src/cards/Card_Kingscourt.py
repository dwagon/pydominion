from Card import Card


class Card_Kingscourt(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Play action 3 times"
        self.name = "King's Court"
        self.cost = 7

    def special(self, game, player):
        """ You may chose an Action card in your hand. Play it three times """
        options = [{'selector': '0', 'print': "Don't play a card", 'card': None}]
        index = 1
        for c in player.hand:
            if not c.isAction():
                continue
            sel = "%d" % index
            pr = "Play %s trice" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Play which action card three times?")
        if not o['card']:
            return
        for i in range(1, 4):
            player.output("Number %d play of %s" % (i, o['card'].name))
            player.playCard(o['card'], discard=False, costAction=False)
        player.discardCard(o['card'])

#EOF
