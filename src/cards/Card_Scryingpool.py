from Card import Card


class Card_Scryingpool(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.desc = "+1 action, potentially discard others top cards, get lots of cards into hand"
        self.name = 'Scrying Pool'
        self.actions = 1
        self.cost = 2
        self.potcost = 1

    def special(self, game, player):
        """ Each player (including you) reveals the top card of his
            deck and their discards it or puts it back, your choice.
            Then reveal cards from the top of your deck until you reveal
            on that is not an Action. Put all of your revealed cards
            into your hand."""
        for plr in game.players:
            if not plr.hasDefense():
                self.discardOrPutBack(plr, player)
        while(1):
            topcard = player.pickupCard()
            if not topcard.isAction():
                break

    def discardOrPutBack(self, victim, player):
        topcard = victim.nextCard()
        options = [
            {'selector': '0', 'print': 'Discard %s' % topcard.name, 'action': 'discard'},
            {'selector': '1', 'print': 'Putback %s' % topcard.name, 'action': 'putback'},
            ]
        o = player.userInput(options, "For %s which one?" % victim.name)
        if o['action'] == 'discard':
            victim.addCard(topcard, 'discard')
        else:
            victim.addCard(topcard, 'deck')


#EOF
