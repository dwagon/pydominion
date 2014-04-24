from Card import Card


class Card_Torturer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+3 cards; Other players discard 2 cards or gain a curse"
        self.needcurse = True
        self.name = 'Torturer'
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        """ Each other player chooses one: he discards 2 cards; or
            he gains a Curse card, putting it in his hand """
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense():
                print "Player %s is defended" % plr.name
                continue
            print "*" * 20
            print "Player %s - Choose:" % plr.name
            self.choiceOfDoom(plr)
            print "*" * 20

    def choiceOfDoom(self, victim):
        options = [
            {'selector': '0', 'print': 'Discard 2 cards', 'choice': 'discard'},
            {'selector': '1', 'print': 'Gain a curse card', 'choice': 'curse'}
            ]
        o = victim.userInput(options, "Discard or curse")
        if o['choice'] == 'discard':
            victim.plrDiscardCards(2)
        else:
            victim.gainCard('curse')

#EOF
