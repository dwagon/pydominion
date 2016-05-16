class Card(object):
    def __init__(self):
        self.image = None
        self.desc = "TODO"
        self.name = "TODO"
        self.base = "TODO"
        self.basecard = False
        self.stacksize = 10
        self.cost = -1
        self.potcost = 0
        self.cardtype = 'unknown'
        self.purchasable = True
        self.playable = True
        self.callable = True
        self.defense = False
        self.needcurse = False
        self.needspoils = False
        self.traveller = False
        self.when = 'any'
        self.actions = 0
        self.buys = 0
        self.coin = 0
        self.potion = 0
        self.cards = 0
        self.victory = 0
        self.cardname = self.getCardName()
        self.image = self.getImageName()

    def getCardName(self):
        c = self.__class__.__name__
        c = c.replace('Card_', '')
        return c.lower()

    def __repr__(self):
        return self.name

    def getImageName(self):
        return 'images/%s.jpg' % self.cardname

    def special(self, game, player):
        pass    # pragma: no cover

    def duration(self, game, player):
        pass    # pragma: no cover

    def setup(self, game):
        pass    # pragma: no cover

    def hasDefense(self):
        return self.defense

    def isDuration(self):
        if 'duration' in self.cardtype:
            return True
        return False

    def isTreasure(self):
        if 'treasure' in self.cardtype:
            return True
        return False

    def isLooter(self):
        if 'looter' in self.cardtype:
            return True
        return False

    def isAction(self):
        if 'action' in self.cardtype:
            return True
        return False

    def isShelter(self):
        if 'shelter' in self.cardtype:
            return True
        return False

    def isRuin(self):
        if 'ruin' in self.cardtype:
            return True
        return False

    def isTraveller(self):
        if 'traveller' in self.cardtype:
            return True
        return False

    def isVictory(self):
        if 'victory' in self.cardtype:
            return True
        return False

    def isReaction(self):
        if 'reaction' in self.cardtype:
            return True
        return False

    def isKnight(self):
        if 'knight' in self.cardtype:
            return True
        return False

    def isAttack(self):
        if 'attack' in self.cardtype:
            return True
        return False

    def isReserve(self):
        if 'reserve' in self.cardtype:
            return True
        return False

    def special_score(self, game, player):
        return 0    # pragma: nocover

    def hook_buyCard(self, game, player, card):
        pass    # pragma: no cover

    def hook_buyThisCard(self, game, player):
        pass    # pragma: no cover

    def hook_callReserve(self, game, player):
        pass    # pragma: no cover

    def hook_allowedToBuy(self, game, player):
        return True     # pragma: no cover

    def hook_gainCard(self, game, player, card):
        return {}   # pragma: no cover

    def hook_cardCost(self, game, player, card):
        return 0    # pragma: no cover

    def hook_coinvalue(self, game, player):
        """ How much coin does this card contribute """
        return self.coin    # pragma: no cover

    def hook_spendValue(self, game, player, card):
        """ Does this card make any  modifications on the value of spending a card """
        return 0    # pragma: no cover

    def hook_underAttack(self, game, player):
        pass    # pragma: no cover

    def hook_discardCard(self, game, player):
        pass    # pragma: no cover

    def hook_trashThisCard(self, game, player):
        pass    # pragma: no cover

    def hook_gainThisCard(self, game, player):
        pass    # pragma: no cover

    def knight_special(self, game, player):
        """ Each other player reveals the top 2 cards of his deck,
            trashes one of them costing from 3 to 6 and discards the
            rest. If a knight is trashed by this, trash this card """
        for pl in game.players:
            if pl == player:
                continue
            if pl.hasDefense():
                continue
            self.knight_attack(game, player, pl)

    def knight_attack(self, game, player, victim):
        cards = []
        for i in range(2):
            c = victim.nextCard()
            if 3 <= c.cost <= 6:
                cards.append(c)
            else:
                victim.discardCard(c)
        if not cards:
            return
        index = 0
        options = []
        for c in cards:
            sel = '%d' % index
            index += 1
            options.append({'selector': sel, 'print': 'Trash %s' % c.name, 'card': c})
        o = victim.userInput(options, "Trash a card due to %s's %s" % (player.name, self.name))
        if o['card'].isKnight():
            player.output("%s trashed a knight: %s - trashing your %s" % (victim.name, o['card'].name, self.name))
            player.trashCard(self)
        victim.trashCard(o['card'])
        for c in cards:
            if c != o['card']:
                victim.discardCard(c)

# EOF
