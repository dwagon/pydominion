import imp


class CardPile(object):
    def __init__(self, cardname, numcards=10, cardpath='cards'):
        self.cardpath = cardpath
        cardmodule = self.importCard(cardname=cardname)
        self.cardclass = getattr(cardmodule, "Card_%s" % cardname)
        self.card = self.cardclass()
        self.cardname = cardname
        self.numcards = numcards

    def importCard(self, cardname=None, cardfile=None):
        if cardfile:
            fp, pathname, desc = imp.find_module(cardfile, [self.cardpath, 'cards'])
        else:
            try:
                fp, pathname, desc = imp.find_module("Card_%s" % cardname, [self.cardpath, 'cards'])
            except ImportError:
                fp, pathname, desc = imp.find_module("BaseCard_%s" % cardname, [self.cardpath, 'cards'])
        cardmodule = imp.load_module(cardname, fp, pathname, desc)
        return cardmodule

    def __getattr__(self, name):
        return getattr(self.card, name)

    def isEmpty(self):
        return self.numcards == 0

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.cardclass()
        else:
            return None

    def add(self):
        self.numcards += 1

    def __repr__(self):
        return "CardPile %s: %d" % (self.name, self.numcards)

#EOF
