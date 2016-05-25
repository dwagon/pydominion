

###############################################################################
class CardPile(object):
    def __init__(self, cardname, klass, numcards=10, cardpath='cards'):
        self.cardpath = cardpath
        self.cardname = cardname
        self.numcards = numcards
        self.cardclass = klass
        self.card = klass()

    ###########################################################################
    def __lt__(self, a):
        return self.cardname < a.cardname

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.card, name)

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
        return "CardPile %s: %d" % (self.name, self.numcards)

# EOF
