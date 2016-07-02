class Card(object):
    def __init__(self):
        self.image = None
        self.desc = "TODO"
        self.name = "TODO"
        self.base = "TODO"
        self.basecard = False
        self.cost = -1
        self.debtcost = 0
        self.potcost = False
        self.cardtype = 'unknown'
        self.purchasable = True
        self.permanent = False
        self.playable = True
        self.callable = True
        self.defense = False
        self.needsprize = False
        self.overpay = False
        self.traveller = False
        self.when = 'any'
        self.actions = 0
        self.buys = 0
        self.coin = 0
        self.potion = 0
        self.cards = 0
        self.victory = 0
        self.required_cards = []
        self.image = None
        self.numcards = 10

    def __repr__(self):
        return self.name

    def __lt__(self, card):
        return self.name < card.name

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

    def isDebt(self):
        return self.debtcost != 0

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

    def hook_postAction(self, game, player):
        pass    # pragma: no cover

    def hook_cleanup(self, game, player):
        pass    # pragma: no cover

    def hook_allPlayers_buyCard(self, game, player, owner, card):
        pass    # pragma: no cover

    def hook_buyCard(self, game, player, card):
        pass    # pragma: no cover

    def hook_buyThisCard(self, game, player):
        pass    # pragma: no cover

    def hook_callReserve(self, game, player):
        pass    # pragma: no cover

    def hook_allowedToBuy(self, game, player):
        return True     # pragma: no cover

    def hook_allPlayers_gainCard(self, game, player, owner, card):
        pass    # pragma: no cover

    def hook_gainCard(self, game, player, card):
        return {}   # pragma: no cover

    def hook_cardCost(self, game, player, card):
        return 0    # pragma: no cover

    def hook_thisCardCost(self, game, player):
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

    def hook_trashCard(self, game, player, card):
        pass    # pragma: no cover

    def hook_gainThisCard(self, game, player):
        return {}    # pragma: no cover

    def hook_endTurn(self, game, player):
        pass    # pragma: no cover

    def hook_end_of_game(self, game, player):
        pass    # pragma: no cover

# EOF
