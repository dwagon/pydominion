

###############################################################################
class CardPile(object):
    def __init__(self, cardname, klass, game, cardpath='cards'):
        self.cardpath = cardpath
        self.cardname = cardname
        self.cardclass = klass
        self.card = klass()
        self.embargo_level = 0
        if hasattr(self.card, 'calc_numcards'):
            self.pilesize = self.card.calc_numcards(game)
        else:
            self.pilesize = self.card.numcards
        print("{} {}".format(self.card.name, self.pilesize))

    ###########################################################################
    def embargo(self):
        self.embargo_level += 1

    ###########################################################################
    def __lt__(self, a):
        return self.card.name < a.card.name

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.card, name)

    ###########################################################################
    def isEmpty(self):
        return self.pilesize == 0

    ###########################################################################
    def remove(self):
        if self.pilesize:
            self.pilesize -= 1
            return self.cardclass()
        else:
            return None

    ###########################################################################
    def add(self):
        self.pilesize += 1

    ###########################################################################
    def __repr__(self):
        return "CardPile %s: %d" % (self.name, self.pilesize)

# EOF
