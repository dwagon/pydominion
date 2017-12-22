from CardPile import CardPile


###############################################################################
class SplitCardPile(CardPile):
    def __init__(self, cardname, klass, game, cardpath='cards'):
        CardPile.__init__(self, cardname, klass, game, cardpath)
        self.top_pile = self
        self.bottom_pile = self.split

    ###########################################################################
    def isEmpty(self):
        return self.numcards == 0

    ###########################################################################
    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.cardclass()
        else:
            return None

    ###########################################################################
    def add(self):
        self.numcards += 1

    ###########################################################################
    def __repr__(self):
        return "SplitCardPile %s: %d" % (self.name, self.numcards)

# EOF
