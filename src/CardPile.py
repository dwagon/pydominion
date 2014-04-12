import imp

class CardPile(object):
    def __init__(self, cardname, numcards=10):
        self.cardname = cardname
        self.numcards = numcards
        try:
            fp, pathname, description = imp.find_module("Card_%s" % self.cardname, ['cards'])
        except ImportError:
            fp, pathname, description = imp.find_module("BaseCard_%s" % self.cardname, ['cards'])
        cardmodule = imp.load_module(cardname, fp, pathname, description)
        self.cardclass = getattr(cardmodule, "Card_%s" % self.cardname)

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.cardclass()
        else:
            print "Pile %s is empty" % self.cardname

    def __repr__(self):
        return "CardPile %s: %d" % (self.cardname, self.numcards)

#EOF
