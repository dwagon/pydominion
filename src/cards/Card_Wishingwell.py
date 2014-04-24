from Card import Card


class Card_Wishingwell(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +1 action, guess top card to get it"
        self.name = 'Wishing Well'
        self.cost = 3

    def special(self, game, player):
        """" Name a card. Reveal the top card of your deck. If it's
            the named card, put it into your hand """
        options = [{'selector': '0', 'print': 'No guess', 'card': None}]
        index = 1
        for c in game.cardTypes():
            sel = "%s" % index
            options.append({'selector': sel, 'print': "Guess %s" % c.name, 'card': c})
            index += 1
        o = player.userInput(options, "Guess the top card")
        if not o['card']:
            return
        c = player.nextCard()
        if o['card'].name == c.name:
            print "You guessed correctly"
            player.addCard(c, 'hand')
        else:
            print "You chose poorly - it was a %s" % c.name
            player.addCard(c, 'deck')

#EOF
