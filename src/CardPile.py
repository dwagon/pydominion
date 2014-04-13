import imp

class CardPile(object):
    def __init__(self, cardname, numcards=10):
        self.name = cardname
        self.numcards = numcards
        try:
            fp, pathname, description = imp.find_module("Card_%s" % self.name, ['cards'])
        except ImportError:
            fp, pathname, description = imp.find_module("BaseCard_%s" % self.name, ['cards'])
        cardmodule = imp.load_module(self.name, fp, pathname, description)
        self.cardclass = getattr(cardmodule, "Card_%s" % self.name)
        self.card = self.cardclass()

    def __getattr__(self, name):
        return getattr(self.card, name)

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.cardclass()
        else:
            print "Pile %s is empty" % self.name
            return None

    def __repr__(self):
        return "CardPile %s: %d" % (self.name, self.numcards)

#EOF
