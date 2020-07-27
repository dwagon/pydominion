# pylint: disable=no-member
class Card(object):
    def __init__(self):
        self.image = None
        self.name = "TODO"
        self.base = "TODO"
        self.basecard = False
        self.cost = -1
        self.debtcost = 0
        self.always_buyable = False
        self.potcost = False
        self.cardtype = 'unknown'
        self.purchasable = True
        self.permanent = False
        self.playable = True
        self.callable = True
        self.defense = False
        self.needsprize = False
        self.needsartifacts = False
        self.needsprojects = False
        self.overpay = False
        self.insupply = True
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
        self.gatheredvp = 0
        self.retain_boon = False
        self.heirloom = None

    ##########################################################################
    def get_cardtype_repr(self):
        if isinstance(self.cardtype, str):
            ct = [self.cardtype]
        else:
            ct = self.cardtype[:]
        return ", ".join([_.title() for _ in ct])

    ##########################################################################
    def __repr__(self):
        return self.name

    ##########################################################################
    def __lt__(self, card):
        return self.name < card.name

    ##########################################################################
    def description(self, player):
        if callable(self.desc):
            return self.desc(player)
        return self.desc

    ##########################################################################
    def addVP(self, num=1):
        self.gatheredvp += num

    ##########################################################################
    def getVP(self):
        return self.gatheredvp

    ##########################################################################
    def drainVP(self):
        num = self.gatheredvp
        self.gatheredvp = 0
        return num

    ##########################################################################
    def special(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def night(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def duration(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def setup(self, game):
        pass    # pragma: no cover

    ##########################################################################
    def hasDefense(self):
        return self.defense

    ##########################################################################
    def isGathering(self):
        if 'gathering' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isDuration(self):
        if 'duration' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isDebt(self):
        return self.debtcost != 0

    ##########################################################################
    def isTreasure(self):
        if 'treasure' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isNight(self):
        if 'night' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isFate(self):
        if 'fate' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isDoom(self):
        if 'doom' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isLooter(self):
        if 'looter' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isAction(self):
        if 'action' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isShelter(self):
        if 'shelter' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isRuin(self):
        if 'ruin' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isTraveller(self):
        if 'traveller' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isVictory(self):
        if 'victory' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isReaction(self):
        if 'reaction' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isCastle(self):
        if 'castle' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isKnight(self):
        if 'knight' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isAttack(self):
        if 'attack' in self.cardtype:
            return True
        return False

    ##########################################################################
    def isReserve(self):
        if 'reserve' in self.cardtype:
            return True
        return False

    ##########################################################################
    def special_score(self, game, player):
        return 0    # pragma: nocover

    ##########################################################################
    def hook_cleanup(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_allPlayers_preAction(self, game, player, owner, card):
        pass    # pragma: no cover

    ##########################################################################
    def hook_allPlayers_buyCard(self, game, player, owner, card):
        pass    # pragma: no cover

    ##########################################################################
    def hook_buyCard(self, game, player, card):
        pass    # pragma: no cover

    ##########################################################################
    def hook_buy_this_card(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_call_reserve(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_allowedToBuy(self, game, player):
        return True     # pragma: no cover

    ##########################################################################
    def hook_allPlayers_gainCard(self, game, player, owner, card):
        pass    # pragma: no cover

    ##########################################################################
    def hook_gain_card(self, game, player, card):
        return {}   # pragma: no cover

    ##########################################################################
    def hook_cardCost(self, game, player, card):
        return 0    # pragma: no cover

    ##########################################################################
    def hook_this_card_cost(self, game, player):
        return 0    # pragma: no cover

    ##########################################################################
    def hook_coinvalue(self, game, player):
        """ How much coin does this card contribute """
        return self.coin    # pragma: no cover

    ##########################################################################
    def hook_spendValue(self, game, player, card):
        """ Does this card make any  modifications on the value of spending a card """
        return 0    # pragma: no cover

    ##########################################################################
    def hook_underAttack(self, game, player, attacker):
        pass    # pragma: no cover

    ##########################################################################
    def hook_discardThisCard(self, game, player, source):
        pass    # pragma: no cover

    ##########################################################################
    def hook_trashThisCard(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_trash_card(self, game, player, card):
        pass    # pragma: no cover

    ##########################################################################
    def hook_gain_this_card(self, game, player):
        return {}    # pragma: no cover

    ##########################################################################
    def hook_end_turn(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_end_of_game(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_preBuy(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_endBuyPhase(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_startTurn(self, game, player):
        pass    # pragma: no cover

    ##########################################################################
    def hook_revealThisCard(self, game, player):
        pass    # pragma: no cover

# EOF
