from Card import Card


class Card_Tribute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Player to left discards 2 cards; you get goodies"
        self.name = 'Tribute'
        self.cost = 5

    def special(self, game, player):
        """ The player to your left reveals then discards the top
            2 cards of his deck. For each differently named card revealed,
            if is an Action card, +2 actions; treasure card, +2 gold;
            victory card, +2 cards """
        victim = game.playerToLeft(player)
        cards = [victim.nextCard(), victim.nextCard()]
        cardname = None
        for c in cards:
            print("Looking at %s from %s" % (c.name, victim.name))
            victim.addCard(c, 'discard')
            if c.name == cardname:
                continue
            cardname = c.name
            if c.isAction():
                print("Gained two actions")
                player.t['actions'] += 2
            elif c.isTreasure():
                print("Gained two gold")
                player.t['gold'] += 2
            elif c.isVictory():
                for i in range(2):
                    n = player.pickupCard()

#EOF
