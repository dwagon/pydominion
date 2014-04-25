from Card import Card


class Card_Courtyard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+3 actions. Put a card from hand to top of deck"
        self.name = 'Courtyard'
        self.cards = 3
        self.cost = 2

    def special(self, player, game):
        """ Put a card from your hand on top of your deck """
        options = [{'selector': '0', 'print': "Don't put anything on deck", 'card': None}]
        index = 1
        for c in player.hand:
            sel = "%d" % index
            pr = "Put %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Put which card on top of deck?")
        if not o['card']:
            return
        player.addCard(o['card'], 'deck')
        player.output("Put %s on top of deck" % o['card'].name)

#EOF
