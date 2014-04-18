from Card import Card


class Card_Bureaucrat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Gain a silver"
        self.name = 'Bureaucrat'
        self.cost = 4

    def special(self, game, player):
        """ Gain a silver card and put it on top of your deck. Each
        other player reveals a victory card from his hand and puts
        it on his deck (or reveals a hand with no victory cards)
        """
        silver = game['Silver']
        player.addCard(silver.remove(), 'deck')

        for pl in game.players:
            if pl == player:
                continue
            if pl.hasDefense():
                print "Player %s is defended" % pl.name
                continue
            for c in pl.hand:
                if c.isVictory():
                    pl.addCard(c, 'deck')
                    print "Player %s moved a %s to the top" % (pl.name, c.name)
                    break

#EOF
