

###############################################################################
class CardPile(object):
    def __init__(self, cardname, klass, numcards=-1, cardpath='cards'):
        self.cardpath = cardpath
        self.cardname = cardname
        self.cardclass = klass
        self.card = klass()
        if numcards < 0:
            self.numcards = self.card.stacksize
        else:
            self.numcards = numcards

    ###########################################################################
    def __lt__(self, a):
        return self.card.name < a.card.name

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
