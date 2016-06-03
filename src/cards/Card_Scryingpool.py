from Card import Card


class Card_Scryingpool(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'alchemy'
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
        for plr in player.attackVictims():
            self.discardOrPutBack(plr, player)
        self.discardOrPutBack(player, player)
        while(1):
            topcard = player.pickupCard()
            if not topcard.isAction():
                break

    def discardOrPutBack(self, victim, player):
        topcard = victim.nextCard()
        putback = player.plrChooseOption(
            "For %s which one?" % victim.name,
            ('Discard %s' % topcard.name, False),
            ('Putback %s' % topcard.name, True))
        if putback:
            victim.addCard(topcard, 'deck')
        else:
            victim.addCard(topcard, 'discard')


# EOF
