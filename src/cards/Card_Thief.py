from Card import Card


class Card_Thief(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Steal treasure from other players"
        self.name = 'Thief'
        self.cost = 4

    def special(self, game, player):
        """ Each other player reveals the top 2 cards of his deck.
            If they revealed any Treasure cards, they trash one them
            that you choose. You may gain any or all of these trashed
            Cards. They discard the other revealed cards. """

        for pl in game.players:
            if pl == player:
                continue
            if pl.hasDefense():
                print "%s is defended" % pl.name
            else:
                self.thieveOn(pl, player)

    def thieveOn(self, victim, thief):
        treasures = []
        for i in range(2):
            c = victim.nextCard()
            if c.isTreasure():
                treasures.append(c)
            else:
                victim.addCard(c, 'discard')
        if not treasures:
            print "Player %s has no treasures" % victim.name
            return
        index = 1
        options = [ {'selector': '0', 'print': "Don't trash any card", 'card': None, 'steal': False} ]
        for c in treasures:
            sel = '%s' % index
            pr = "Trash %s from %s" % (c.name, victim.name)
            options.append({'selector': sel, 'print': pr, 'card': c, 'steal': False})
            index += 1
            sel = '%s' % index
            pr = "Steal %s from %s" % (c.name, victim.name)
            options.append({'selector': sel, 'print': pr, 'card': c, 'steal': False})
            index += 1
        o = victim.userInput(options, "What to do to %s's cards?" % victim.name)
        if not o['card']:
            return
        # Discard the ones we don't care about
        for tc in treasures:
            if o['card'] != tc:
                victim.discardCard(tc)
        if o['steal']:
            thief.addCard(o['card'])
            print "Stealing %s form %s" % (o['card'].name, victim.name)
        else:
            victim.trashCard(o['card'])

#EOF
