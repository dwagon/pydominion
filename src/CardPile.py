import imp


class CardPile(object):
    def __init__(self, cardname, numcards=10, cardpath='cards'):
        try:
            fp, pathname, description = imp.find_module("Card_%s" % cardname, [cardpath, 'cards'])
        except ImportError:
            fp, pathname, description = imp.find_module("BaseCard_%s" % cardname, [cardpath, 'cards'])
        cardmodule = imp.load_module(cardname, fp, pathname, description)
        self.cardclass = getattr(cardmodule, "Card_%s" % cardname)
        self.card = self.cardclass()
        self.cardname = cardname
        self.numcards = numcards

    def __getattr__(self, name):
        return getattr(self.card, name)

    def isEmpty(self):
        return self.numcards == 0

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.cardclass()
        else:
            print("No more %s available" % self.name)
            return None

    def __repr__(self):
        return "CardPile %s: %d" % (self.name, self.numcards)

#EOF
