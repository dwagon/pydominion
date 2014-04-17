from Card import Card


class Card_Chancellor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 gold, Discard deck"
        self.name = 'chancellor'
        self.image = 'images/chancellor.jpg'
        self.gold = 2
        self.cost = 3

    def special(self, game, player):
        """ You may immediately put your deck into your discard pile """
        options = [
            {'selector': '0', 'print': "Don't Discard Deck", 'discard': False},
            {'selector': '1', 'print': "Discard Deck", 'discard': True}
            ]
        o = player.userInput(options, "Discard deck?")
        if o['discard']:
            # The equivalent of putting the deck into the discard
            # pile is putting the discard into the deck and
            # shuffling
            for c in player.discardpile[:]:
                player.addCard(c, 'deck')
            player.shuffleDeck()
            return

#EOF
