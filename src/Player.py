from PlayArea import PlayArea
# from Card import Card
# from CardPile import CardPile
import operator
import random
import sys

playerNames = ['Adam', 'Alan', 'Alexander', 'Amanda', 'Amy', 'Andrew', 'Angela',
               'Anne', 'Anthony', 'Barbara', 'Benjamin', 'Brian',
               'Catherine', 'Chloe', 'Christine', 'Christopher',
               'Colin', 'Craig', 'Daniel', 'Darren', 'David',
               'Elizabeth', 'Emily', 'Emma', 'Fiona', 'Gary',
               'Geoffrey', 'George', 'Graeme', 'Gregory', 'Heather',
               'Helen', 'Ian', 'Jack', 'James', 'Jason', 'Jennifer',
               'Jessica', 'Joan', 'Joanne', 'John', 'Joshua',
               'Judith', 'Julie', 'Karen', 'Kate', 'Kathleen',
               'Kenneth', 'Kevin', 'Lachlan', 'Laura', 'Lauren',
               'Leanne', 'Linda', 'Lisa', 'Luke', 'Lynette',
               'Margaret', 'Maria', 'Mark', 'Mary', 'Matthew',
               'Melissa', 'Michael', 'Michelle', 'Natalie', 'Nathan',
               'Nicholas', 'Nicole', 'Olivia', 'Pamela', 'Patricia',
               'Paul', 'Peter', 'Raymond', 'Rebecca', 'Richard',
               'Robert', 'Robyn', 'Ronald', 'Ryan', 'Samantha',
               'Samuel', 'Sandra', 'Sarah', 'Scott', 'Shane',
               'Sharon', 'Shirley', 'Simon', 'Stephanie', 'Stephen',
               'Steven', 'Susan', 'Suzanne', 'Thomas', 'Timothy',
               'Wayne', 'Wendy', 'William']


###############################################################################
###############################################################################
###############################################################################
class Player(object):
    def __init__(self, game, name='', quiet=False):
        self.game = game
        if not name:
            name = random.choice(playerNames)
        game.output("Player %s is at the table" % name)
        self.score = {}
        self.name = name
        self.specialcoins = 0
        self.messages = []
        self.hand = PlayArea([])
        self.durationpile = PlayArea([])
        self.deck = PlayArea([])
        self.played = PlayArea([])
        self.discardpile = PlayArea([])
        self.buys = 1
        self.actions = 1
        self.coin = 0
        self.potions = 0
        self.handsize = 5
        self.card_token = False
        self.coin_token = False
        self.journey_token = True
        self.quiet = quiet
        self.test_input = []
        self.initial_Deck()
        self.initial_tokens()
        self.once = {}
        self.pickUpHand()

    ###########################################################################
    def initial_Deck(self):
        """ Provide the initial deck - cards don't come from the piles
            hence add them back """
        self.game['Copper'].numcards += 7
        for i in range(7):
            self.deck.add(self.game['Copper'].remove())
        self.game['Estate'].numcards += 3
        for i in range(3):
            self.deck.add(self.game['Estate'].remove())
        self.deck.shuffle()

    ###########################################################################
    def initial_tokens(self):
        self.tokens = {
            'Trashing': None,
            'Estate': None,
            '+Card': None,
            '+Action': None,
            '+Buy': None,
            '+Coin': None,
            '-Cost': None,
            # '-Card': Handled elsewhere
            # 'Journey': Handled elsewhere
            # '-Coin': Handled elsewhere
        }

    ###########################################################################
    def flip_journey_token(self):
        if self.journey_token:
            self.journey_token = False
        else:
            self.journey_token = True
        return self.journey_token

    ###########################################################################
    def do_once(self, card):
        """ Allow a player to do something once per turn """
        if card in self.once:
            return False
        self.once[card] = True
        return True

    ###########################################################################
    def place_token(self, token, pilename):
        """ Place a token on a pile
            Can pass the card, the cardpile or just the name """
        if hasattr(pilename, 'name'):
            pilename = pilename.name
        self.tokens[token] = pilename

    ###########################################################################
    def which_token(self, pilename):
        """ Return which token(s) are on a cardstack """
        if hasattr(pilename, 'name'):
            pilename = pilename.name
        onstack = []
        for tk in self.tokens:
            if self.tokens[tk] == pilename:
                onstack.append(tk)
        return onstack

    ###########################################################################
    def inHand(self, cardname):
        """ Return named card if cardname is in hand """
        # assert(isinstance(cardname, str))
        for c in self.hand:
            if c.cardname == cardname.lower():
                return c
        return None

    ###########################################################################
    def trashCard(self, c):
        """ Take a card out of the game """
        c.hook_trashThisCard(game=self.game, player=self)
        self.game.trashpile.add(c)
        if c in self.played:
            self.played.remove(c)
        if c in self.hand:
            self.hand.remove(c)

    ###########################################################################
    def setPlayed(self, *cards):
        """ This is mostly used for testing """
        self.played.empty()
        for c in cards:
            self.played.add(self.game[c].remove())

    ###########################################################################
    def setDiscard(self, *cards):
        """ This is mostly used for testing """
        self.discardpile.empty()
        for c in cards:
            self.discardpile.add(self.game[c].remove())

    ###########################################################################
    def setHand(self, *cards):
        """ This is mostly used for testing """
        self.hand.empty()
        for c in cards:
            self.hand.add(self.game[c].remove())

    ###########################################################################
    def setDeck(self, *cards):
        """ This is mostly used for testing """
        self.deck.empty()
        for c in cards:
            self.deck.add(self.game[c].remove())

    ###########################################################################
    def nextCard(self):
        """ Return the next card from the deck """
        if not self.deck:
            self.shuffleDeck()
            while self.discardpile:
                self.addCard(self.discardpile.topcard(), 'deck')
        if not self.deck:
            self.output("No more cards in deck")
            return None
        c = self.deck.topcard()
        return c

    ###########################################################################
    def pickupCards(self, num, verbose=True, verb='Picked up'):
        cards = []
        for i in range(num):
            cards.append(self.pickupCard(verbose=verbose, verb=verb))
        return cards

    ###########################################################################
    def pickupCard(self, card=None, verbose=True, verb='Picked up'):
        """ Pick a card from the deck and put it into the players hand """
        if not card:
            card = self.nextCard()
            if not card:
                self.output("No more cards to pickup")
                return None
        self.addCard(card, 'hand')
        if verbose:
            self.output("%s %s" % (verb, card.name))
        return card

    ###########################################################################
    def shuffleDeck(self):
        self.output("Shuffling Pile of %d cards" % len(self.discardpile))
        self.discardpile.shuffle()

    ###########################################################################
    def pickUpHand(self, handsize=None):
        if handsize is None:
            handsize = self.handsize
        if self.card_token:
            self.output("-Card token reduce draw by one")
            handsize -= 1
            self.card_token = False
        while self.handSize() < handsize:
            c = self.pickupCard(verb='Dealt')
            if not c:
                self.output("Not enough cards to fill hand")
                break

    ###########################################################################
    def gainSpecialCoins(self, num=1):
        """ Gain a number of coin tokens """
        self.specialcoins += num

    ###########################################################################
    def addCard(self, c, pile='discard'):
        if not c:
            return
        if pile == 'discard':
            self.discardpile.add(c)
        elif pile == 'hand':
            self.hand.add(c)
        elif pile == 'topdeck':
            self.deck.add(c)
        elif pile == 'deck':
            self.deck.addToTop(c)
        elif pile == 'played':
            self.played.add(c)
        elif pile == 'duration':
            self.durationpile.add(c)

    ###########################################################################
    def discardCard(self, c):
        if c in self.hand:
            self.hand.remove(c)
        self.addCard(c, 'discard')

    ###########################################################################
    def handSize(self):
        return len(self.hand)

    ###########################################################################
    def playedSize(self):
        return len(self.played)

    ###########################################################################
    def durationSize(self):
        return len(self.durationpile)

    ###########################################################################
    def deckSize(self):
        return len(self.deck)

    ###########################################################################
    def discardSize(self):
        return len(self.discardpile)

    ###########################################################################
    def discardHand(self):
        for c in self.hand + self.played:
            self.hook_discardCard(c)
        while self.hand:
            self.discardCard(self.hand.topcard())
        while self.played:
            self.discardCard(self.played.topcard())

    ###########################################################################
    def playableSelection(self, index):
        options = []
        playable = [c for c in self.hand if c.playable]
        for p in playable:
            sel = chr(ord('a') + index)
            pr = "Play %s (%s)" % (p.name, p.desc)
            options.append({'selector': sel, 'print': pr, 'card': p, 'action': 'play'})
            index += 1
        return options, index

    ###########################################################################
    def spendableSelection(self, index):
        options = []
        spendable = [c for c in self.hand if c.isTreasure()]
        if spendable:
            sel = chr(ord('a') + index)
            totcoin = sum([self.hook_spendValue(c) for c in spendable])
            numpots = sum([1 for c in spendable if c.name == 'Potion'])
            potstr = ", %d potions" % numpots if numpots else ""
            tp = 'Spend all treasures (%d coin%s)' % (totcoin, potstr)
            options.append({'selector': sel, 'print': tp, 'card': None, 'action': 'spendall'})
            index += 1
        for s in spendable:
            sel = chr(ord('a') + index)
            tp = 'Spend %s (%d coin)' % (s.name, self.hook_spendValue(s))
            options.append({'selector': sel, 'print': tp, 'card': s, 'action': 'spend'})
            index += 1

        for c in self.hand:
            if c.name == 'Potion':
                sel = chr(ord('a') + index)
                tp = 'Spend %s' % s.name
                options.append({'selector': sel, 'print': tp, 'card': s, 'action': 'spend'})
                index += 1
        return options, index

    ###########################################################################
    def eventSelection(self, index):
        options = []
        for op in self.game.events.values():
            if op.cost <= self.coin:
                sel = chr(ord('a') + index)
                tp = 'Use event %s: %s (%d coins)' % (op.name, op.desc, op.cost)
                index += 1
                options.append({'selector': sel, 'print': tp, 'card': op, 'action': 'event'})

        return options, index

    ###########################################################################
    def buyableSelection(self, index):
        options = []
        buyable = self.cardsUnder(coin=self.coin, potions=self.potions)
        for p in buyable:
            if not self.hook_allowedToBuy(p):
                continue
            sel = chr(ord('a') + index)
            tp = 'Buy %s (%s) %s (%d left)' % (p.name, self.coststr(p), p.desc, p.numcards)
            for tkn in self.which_token(p):
                tp += "[Tkn: %s]" % tkn
            options.append({'selector': sel, 'print': tp, 'card': p, 'action': 'buy'})
            index += 1
        return options, index

    ###########################################################################
    def choiceSelection(self):
        options = [{'selector': '0', 'print': 'End Turn', 'card': None, 'action': 'quit'}]

        if self.specialcoins:
            options.append({'selector': '1', 'print': 'Spend Coin', 'card': None, 'action': 'coin'})

        index = 0
        if self.actions:
            op, index = self.playableSelection(index)
            options.extend(op)

        if self.buys:
            op, index = self.spendableSelection(index)
            options.extend(op)
            op, index = self.buyableSelection(index)
            options.extend(op)

        if self.game.events and self.buys:
            op, index = self.eventSelection(index)
            options.extend(op)

        prompt = "What to do (actions=%d buys=%d" % (self.actions, self.buys)
        if self.coin:
            prompt += " coin=%d" % self.coin
        if self.potions:
            prompt += " potions=%d" % self.potions
        if self.specialcoins:
            prompt += " specialcoins=%d" % self.specialcoins
        prompt += ")?"
        return self.userInput(options, prompt)

    ###########################################################################
    def addScore(self, reason, points):
        if reason not in self.score:
            self.score[reason] = 0
        self.score[reason] += points

    ###########################################################################
    def allCards(self):
        """ Return all the cards that the player has """
        x = PlayArea([])
        x += self.discardpile
        x += self.hand
        x += self.deck
        x += self.played
        x += self.durationpile
        return x

    ###########################################################################
    def getScoreDetails(self, verbose=False):
        scr = {}
        for c in self.allCards():
            scr[c.name] = scr.get(c.name, 0) + c.victory
            scr[c.name] = scr.get(c.name, 0) + c.special_score(self.game, self)
        scr.update(self.score)
        return scr

    ###########################################################################
    def getScore(self, verbose=False):
        scr = self.getScoreDetails(verbose)
        vp = sum(scr.values())
        if verbose:
            self.game.output("%s: %s" % (self.name, scr))
        return vp

    ###########################################################################
    def hook_allowedToBuy(self, card):
        """ Hook to check if you are allowed to buy a card """
        return card.hook_allowedToBuy(game=self.game, player=self)

    ###########################################################################
    def hook_buyCard(self, card):
        """ Hook for after purchasing a card """
        for c in self.played:
            c.hook_buyCard(game=self.game, player=self, card=card)

    ###########################################################################
    def startTurn(self):
        self.played.empty()
        self.buys = 1
        self.actions = 1
        self.coin = 0
        self.potions = 0
        for card in self.durationpile:
            card.duration(game=self.game, player=self)
            self.addCard(card, 'played')
        self.durationpile.empty()

    ###########################################################################
    def spendCoin(self):
        if self.specialcoins <= 0:
            return
        self.specialcoins -= 1
        self.coin += 1
        self.output("Spent a coin")

    ###########################################################################
    def endTurn(self):
        self.messages = []
        self.once = {}
        self.discardHand()
        self.pickUpHand()
        self.handsize = 5

    ###########################################################################
    def hook_discardCard(self, card):
        """ A card has been discarded """
        card.hook_discardCard(game=self.game, player=self)

    ###########################################################################
    def hook_spendValue(self, card):
        """ How much do you get for spending the card """
        val = card.hook_coinvalue(game=self.game, player=self)
        for c in self.played:
            val += c.hook_spendValue(game=self.game, player=self, card=card)
        if self.coin_token:
            val -= 1
            self.coin_token = False
        return val

    ###########################################################################
    def spendAllCards(self):
        for card in self.hand[:]:
            if card.isTreasure():
                self.playCard(card)

    ###########################################################################
    def playCard(self, card, discard=True, costAction=True):
        # assert(isinstance(card, (Card, CardPile)))
        if card.isAction() and costAction:
            self.actions -= 1
        if self.actions < 0:
            self.actions = 0
            return
        self.output("Played %s" % card.name)
        tkns = self.which_token(card.name)
        if '+Action' in tkns:
            self.output("Gaining action from +Action token")
            self.actions += 1
        if '+Card' in tkns:
            c = self.pickupCard()
            self.output("Picked up %s from +Card token" % c.name)
        if '+Coin' in tkns:
            self.output("Gaining coin from +Coin token")
            self.coin += 1
        if '+Buy' in tkns:
            self.output("Gaining buy from +Buy token")
            self.buys += 1
        if discard:
            if card.isDuration():
                self.addCard(card, 'duration')
            else:
                self.addCard(card, 'played')
            self.hand.remove(card)
        self.actions += card.actions
        self.coin += self.hook_spendValue(card)
        self.buys += card.buys
        self.potions += card.potion

        modif = 0
        if self.card_token and card.cards:
            self.output("-Card token reduces cards drawn")
            self.card_token = False
            modif = -1

        for i in range(card.cards + modif):
            self.pickupCard()
        try:
            card.special(game=self.game, player=self)
        except KeyboardInterrupt:   # pragma: no cover
            sys.stderr.write("\nFailed: %s\n" % self.messages)
            sys.exit(1)

    ###########################################################################
    def cardCost(self, card):
        cost = card.cost
        if '-Cost' in self.which_token(card):
            cost -= 2
        for c in self.hand + self.played:
            cost += c.hook_cardCost(game=self.game, player=self, card=card)
        return max(0, cost)

    ###########################################################################
    def gainCard(self, cardpile=None, destination='discard', newcard=None):
        """ Add a new card to the players set of cards from a cardpile """
        if not newcard:
            if isinstance(cardpile, str):
                newcard = self.game[cardpile].remove()
            else:
                newcard = cardpile.remove()
        options = self.hook_gainCard(newcard)
        if not newcard:
            sys.stderr.write("ERROR: Getting from empty cardpile %s" % cardpile)
            return
        if 'destination' in options:
            destination = options['destination']
        if 'trash' in options and options['trash']:
            self.trashCard(newcard)
            return newcard
        self.hook_gainThisCard(newcard)
        self.addCard(newcard, destination)
        return newcard

    ###########################################################################
    def buyCard(self, card):
        # assert(isinstance(card, (Card, CardPile)))
        if not self.buys:
            return
        newcard = self.gainCard(card)
        self.buys -= 1
        self.coin -= self.cardCost(newcard)
        self.output("Bought %s for %d coin" % (newcard.name, self.cardCost(newcard)))
        if self.tokens['Trashing'] == card:
            self.output("Trashing token allows you to trash a card")
            self.plrTrashCard()
        self.hook_buyCard(newcard)

    ###########################################################################
    def hook_gainCard(self, card):
        """ Hook which is fired by a card being obtained by a player """
        options = {}
        for c in self.hand:
            o = c.hook_gainCard(game=self.game, player=self, card=card)
            options.update(o)
        return options

    ###########################################################################
    def hook_gainThisCard(self, card):
        """ Hook which is fired by this card being obtained by a player """
        card.hook_gainThisCard(game=self.game, player=self)

    ###########################################################################
    def hasDefense(self, attacker, verbose=True):
        for c in self.hand:
            c.hook_underAttack(game=self.game, player=self)
            if c.hasDefense():
                if verbose:
                    attacker.output("Player %s is defended" % self.name)
                return True
        return False

    ###########################################################################
    def getPotions(self):
        return self.potions

    ###########################################################################
    def getCoin(self):
        return self.coin

    ###########################################################################
    def getSpecialCoins(self):
        return self.specialcoins

    ###########################################################################
    def addCoin(self, num):
        self.coin += num

    ###########################################################################
    def getActions(self):
        return self.actions

    ###########################################################################
    def addActions(self, num):
        self.actions += num

    ###########################################################################
    def getBuys(self):
        return self.buys

    ###########################################################################
    def addBuys(self, num):
        self.buys += num

    ###########################################################################
    def performEvent(self, card):
        self.buys -= 1
        self.coin -= card.cost
        self.output("Using event %s" % card.name)
        card.special(game=self.game, player=self)

    ###########################################################################
    def cardsAffordable(self, oper, coin, potions=0, types={}):
        """Return the list of cards for under cost """
        affordable = PlayArea([])
        for c in self.game.cardTypes():
            cost = self.cardCost(c)
            if not c.purchasable:
                continue
            if c.isAction() and not types['action']:
                continue
            if c.isVictory() and not types['victory']:
                continue
            if c.isTreasure() and not types['treasure']:
                continue
            if not c.numcards:
                continue
            if oper(cost, coin) and oper(c.potcost, potions):
                affordable.add(c)
        affordable.sort(key=lambda c: self.cardCost(c))
        affordable.sort(key=lambda c: c.basecard)
        return affordable

    ###########################################################################
    def cardsUnder(self, coin, potions=0, types={}):
        """Return the list of cards for under cost """
        types = self.typeSelector(types)
        return self.cardsAffordable(operator.le, coin, potions, types)

    ###########################################################################
    def cardsWorth(self, coin, potions=0, types={}):
        """Return the list of cards that are exactly cost """
        types = self.typeSelector(types)
        return self.cardsAffordable(operator.eq, coin, potions, types)

    ###########################################################################
    def countCards(self):
        return len(self.allCards())

    ###########################################################################
    def typeSelector(self, types):
        if not types:
            return {'action': True, 'victory': True, 'treasure': True}
        _types = {'action': False, 'victory': False, 'treasure': False}
        _types.update(types)
        return _types

    ###########################################################################
    def attackVictims(self):
        victims = []
        for plr in list(self.game.players.values()):
            if plr == self:
                continue
            if plr.hasDefense(self):
                continue
            victims.append(plr)
        return victims

    ###########################################################################
    def coststr(self, card):
        coincost = "%d coins" % self.cardCost(card)
        potcost = "%d potions" % card.potcost if card.potcost else ""
        cststr = "%s %s" % (coincost, potcost)
        return cststr.strip()

    ###########################################################################
    def plrTrashCard(self, num=1, anynum=False, printcost=False, force=False, exclude=[]):
        """ Ask player to trash num cards
        """
        if anynum:
            prompt = "Trash any cards"
        else:
            prompt = "Trash %d cards" % num
        trash = self.cardSel(
            num=num, cardsrc='hand', anynum=anynum, printcost=printcost,
            force=force, exclude=exclude, verbs=('Trash', 'Untrash'),
            prompt=prompt)
        for c in trash:
            self.trashCard(c)
        return trash

    ###########################################################################
    def plrGainCard(self, cost, modifier='less', types={}, chooser=None, force=False, destination='discard'):
        """ Gain a card of 'chooser's choice up to cost coin
        if actiononly then gain only action cards
        """
        types = self.typeSelector(types)
        if modifier == 'less':
            prompt = "Gain a card costing up to %d" % cost
            buyable = self.cardsUnder(cost, types=types)
        elif modifier == 'equal':
            prompt = "Gain a card costing exactly %d" % cost
            buyable = self.cardsWorth(cost, types=types)
        buyable = [c for c in buyable if c.purchasable]
        cards = self.cardSel(
            cardsrc=buyable, chooser=chooser, verbs=('Get', 'Unget'),
            force=force, prompt=prompt)
        if cards:
            card = cards[0]
            self.output("Got a %s" % card.name)
            self.addCard(card.remove(), destination)
            return card

    ###########################################################################
    def plrPickCard(self, force=False):
        sel = self.cardSel(force=force)
        return sel[0]

    ###########################################################################
    def plrDiscardCards(self, num=1, anynum=False):
        """ Get the player to discard exactly num cards """
        if anynum:
            msg = "Discard any number of cards"
        else:
            msg = "Discard %d cards" % num
        discard = self.cardSel(
            num=num, anynum=anynum, verbs=('Discard', 'Undiscard'),
            prompt=msg)
        for c in discard:
            self.output("Discarding %s" % c.name)
            self.discardCard(c)
        return discard

    ###########################################################################
    def plrDiscardDownTo(self, num):
        """ Get the player to discard down to num cards in their hand """
        numtogo = len(self.hand) - num
        self.plrDiscardCards(numtogo)

# EOF
