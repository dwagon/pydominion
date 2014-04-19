from Card import Card


class Card_Spy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 cards, reveal next card and optionally discard it"
        self.name = 'Spy'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Each player (including you) reveals the top of his deck and either discards it or puts it back, your choice"""
        for pl in game.players:
            if pl.hasDefense():
                print "%s is defended" % pl.name
            else:
                self.spyOn(pl)

    def spyOn(self, player):
        topcard = player.deck[-1]
        options = [
            {'selector': '0', 'print': "Don't Discard card", 'discard': False},
            {'selector': '1', 'print': "Discard card", 'discard': True}
            ]
        o = player.userInput(options, "Discard %s's %s?" % (player.name, topcard.cardname))
        if o['discard']:
            player.deck.remove(topcard)
            player.addCard(topcard)

#EOF
