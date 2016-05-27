from PlayArea import PlayArea
import operator
import sys
from Card import Card
from CardPile import CardPile
from EventPile import EventPile


###############################################################################
###############################################################################
###############################################################################
class Player(object):
    def __init__(self, game, name):
        self.game = game
        self.name = name
        game.output("Player %s is at the table" % name)
        self.score = {}
        self.specialcoins = 0
        self.messages = []
        self.hand = PlayArea([])
        self.durationpile = PlayArea([])
        self.deck = PlayArea([])
        self.played = PlayArea([])
        self.discardpile = PlayArea([])
        self.reserve = PlayArea([])
        self.buys = 1
        self.actions = 1
        self.coin = 0
        self.potions = 0
        self.newhandsize = 5
        self.card_token = False
        self.coin_token = False
        self.journey_token = True
        self.cleaned = False
        self.is_start = False
        self.test_input = []
        self.initial_Deck()
        self.initial_tokens()
        self.once = {}
        self.stats = {'gain': 0}
        self.pickUpHand()
        self.secret_count = 0   # Hack to count cards that aren't anywhere normal

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
            '+1 Card': None,
            '+1 Action': None,
            '+1 Buy': None,
            '+1 Coin': None,
            '-2 Cost': None,
            # '-1 Card': Handled by card_token
            # 'Journey': Handled by journey_token
            # '-1 Coin': Handled by coin_token
        }

    ###########################################################################
    def replace_traveller(self, src, dst):
        """ For traveller cards replace the src card with a copy of the
        dst card """
        assert(isinstance(src, Card))
        assert(isinstance(dst, str))
        dstcp = None
        for cp in self.game.cardpiles.values():
            if cp.name == dst:
                dstcp = cp
                break
        else:
            assert dstcp is not None, "Couldn't find cardpile %s" % dst

        if src not in self.played:
            self.output("Not activating %s traveller as not played" % src.name)
            return

        choice = self.plrChooseOptions(
            "Replace Traveller",
            ('Keep %s' % src, 'keep'),
            ('Replace with a %s?' % dstcp.name, 'replace')
        )
        if choice == 'keep':
            return
        if choice == 'replace':
            # New card goes into hand as it is about to be discarded

            newcard = self.gainCard(cardpile=dstcp, destination='hand')
            if newcard:
                cardpile = self.game.cardpiles[src.name]
                cardpile.add()
                self.played.remove(src)

    ###########################################################################
    def flip_journey_token(self):
        if self.journey_token:
            self.journey_token = False
        else:
            self.journey_token = True
        return self.journey_token

    ###########################################################################
    def do_once(self, name):
        """ Allow a player to do something once per turn """
        if name in self.once:
            return False
        self.once[name] = True
        return True

    ###########################################################################
    def place_token(self, token, pilename):
        """ Place a token on the specified pile """
        assert(isinstance(pilename, str))
        self.tokens[token] = pilename

    ###########################################################################
    def which_token(self, pilename):
        """ Return which token(s) are on a cardstack """
        assert(isinstance(pilename, str))
        onstack = []
        for tk in self.tokens:
            if self.tokens[tk] == pilename:
                onstack.append(tk)
        return onstack

    ###########################################################################
    def callReserve(self, cardname):
        assert(isinstance(cardname, str))
        c = self.inReserve(cardname)
        if not c:
            self.output("%s not in reserve" % cardname)
            return None
        c.hook_callReserve(game=self.game, player=self)
        self.output("Calling %s from Reserve" % cardname)
        self.reserve.remove(c)
        self.addCard(c, 'discard')
        return c

    ###########################################################################
    def inReserve(self, cardname):
        """ Return named card if cardname is in reserve """
        assert(isinstance(cardname, str))
        for card in self.reserve:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inHand(self, cardname):
        """ Return named card if cardname is in hand """
        assert(isinstance(cardname, str))

        for card in self.hand:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inDiscard(self, cardname):
        """ Return named card if cardname is in the discard pile """
        assert(isinstance(cardname, str))

        for card in self.discardpile:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inPlayed(self, cardname):
        """ Return named card if cardname is in the played pile """
        assert(isinstance(cardname, str))

        for card in self.played:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inDeck(self, cardname):
        """ Return named card if cardname is in the deck pile """
        assert(isinstance(cardname, str))

        for card in self.deck:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def trashCard(self, card):
        """ Take a card out of the game """
        assert(isinstance(card, Card))
        card.hook_trashThisCard(game=self.game, player=self)
        self.game.trashpile.add(card)
        if card in self.played:
            self.played.remove(card)
        if card in self.hand:
            self.hand.remove(card)

    ###########################################################################
    def setReserve(self, *cards):
        """ This is mostly used for testing """
        self.reserve.empty()
        for c in cards:
            self.reserve.add(self.game[c].remove())

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
            self.refill_deck()
        if not self.deck:
            self.output("No more cards in deck")
            return None
        c = self.deck.topcard()
        return c

    ###########################################################################
    def refill_deck(self):
        self.shuffleDeck()
        while self.discardpile:
            self.addCard(self.discardpile.topcard(), 'deck')

    ###########################################################################
    def pickupCards(self, num, verbose=True, verb='Picked up'):
        cards = []
        for i in range(num):
            cards.append(self.pickupCard(verbose=verbose, verb=verb))
        return cards

    ###########################################################################
    def pickupCard(self, card=None, verbose=True, verb='Picked up'):
        """ Pick a card from the deck and put it into the players hand """
        if card is None:
            card = self.nextCard()
            if not card:
                self.output("No more cards to pickup")
                return None
        assert(isinstance(card, Card))
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
            handsize = self.newhandsize
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
    def addCard(self, card, pile='discard'):
        if not card:   # pragma: no cover
            return
        assert(isinstance(card, Card))
        if pile == 'discard':
            self.discardpile.add(card)
        elif pile == 'hand':
            self.hand.add(card)
        elif pile == 'topdeck':
            self.deck.add(card)
        elif pile == 'deck':
            self.deck.addToTop(card)
        elif pile == 'played':
            self.played.add(card)
        elif pile == 'duration':
            self.durationpile.add(card)
        elif pile == 'reserve':
            self.reserve.add(card)

    ###########################################################################
    def discardCard(self, card):
        assert(isinstance(card, Card))
        if card in self.hand:
            self.hand.remove(card)
        self.addCard(card, 'discard')

    ###########################################################################
    def reserveSize(self):
        return len(self.reserve)

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
            for tkn in self.which_token(p.name):
                pr += "[Tkn: %s]" % tkn
            options.append({'selector': sel, 'print': pr, 'card': p, 'action': 'play'})
            index += 1
        return options, index

    ###########################################################################
    def spendableSelection(self):
        options = []
        spendable = [c for c in self.hand if c.isTreasure()]
        totcoin = sum([self.hook_spendValue(c) for c in spendable])
        numpots = sum([1 for c in spendable if c.name == 'Potion'])
        potstr = ", %d potions" % numpots if numpots else ""
        tp = 'Spend all treasures (%d coin%s)' % (totcoin, potstr)
        if spendable:
            options.append({'selector': '1', 'print': tp, 'card': None, 'action': 'spendall'})
        if self.specialcoins:
            options.append({'selector': '2', 'print': 'Spend Coin', 'card': None, 'action': 'coin'})

        index = 3
        for s in spendable:
            tp = 'Spend %s (%d coin)' % (s.name, self.hook_spendValue(s))
            options.append({'selector': str(index), 'print': tp, 'card': s, 'action': 'spend'})
            index += 1

        return options

    ###########################################################################
    def getWhens(self):
        """ Return when we are for calling reserve cards """
        whens = ['any']
        for c in self.played:
            if c.isAction():
                whens.append('postaction')
        if self.is_start:
            whens.append('start')
        return whens

    ###########################################################################
    def reserveSelection(self, index):
        whens = self.getWhens()
        options = []
        for card in self.reserve:
            if not card.callable:
                continue
            if card.when not in whens:
                continue
            sel = chr(ord('a') + index)
            tp = 'Call %s from reserve (%s)' % (card.name, card.desc)
            index += 1
            options.append({'selector': sel, 'print': tp, 'card': card, 'action': 'reserve'})

        return options, index

    ###########################################################################
    def eventSelection(self, index):
        options = []
        for op in self.game.events.values():
            index += 1
            if op.cost <= self.coin:
                sel = chr(ord('a') + index)
                tp = 'Use event %s: %s (%d coins)' % (op.name, op.desc, op.cost)
                action = 'event'
            else:
                sel = '-'
                tp = 'Event %s: %s (%d coins)' % (op.name, op.desc, op.cost)
                action = None
            options.append({'selector': sel, 'print': tp, 'card': op, 'action': action})

        return options, index

    ###########################################################################
    def getAllPurchasable(self):
        """ Return all potentially purchasable cards """
        allcards = PlayArea([])
        for c in self.game.cardTypes():
            if not c.purchasable:
                continue
            allcards.add(c)
        allcards.sort(key=lambda c: self.cardCost(c))
        allcards.sort(key=lambda c: c.basecard)
        return allcards

    ###########################################################################
    def buyableSelection(self, index):
        options = []
        allcards = self.getAllPurchasable()
        buyable = self.cardsUnder(coin=self.coin, potions=self.potions)
        for card in allcards:
            if not self.hook_allowedToBuy(card):
                continue
            sel = chr(ord('a') + index)
            if card in buyable:
                action = 'buy'
                verb = 'Buy %s' % card.name
            else:
                sel = '-'
                action = None
                verb = card.name
            tp = '%s (%s %d left) %s' % (verb, self.coststr(card), card.numcards, card.desc)
            for tkn in self.which_token(card.name):
                tp += "[Tkn: %s]" % tkn
            options.append({'selector': sel, 'print': tp, 'card': card, 'action': action})
            index += 1
        return options, index

    ###########################################################################
    def choiceSelection(self, phase='action'):
        index = 0
        options = [{'selector': '0', 'print': 'End Phase', 'card': None, 'action': 'quit'}]

        if phase == 'action':
            if self.actions:
                op, index = self.playableSelection(index)
                options.extend(op)

        if phase == 'buy':
            if self.buys:
                op = self.spendableSelection()
                options.extend(op)
                op, index = self.buyableSelection(index)
                options.extend(op)
            if self.game.events and self.buys:
                op, index = self.eventSelection(index)
                options.extend(op)

        if self.reserveSize():
            op, index = self.reserveSelection(index)
            options.extend(op)

        status = "Actions=%d Buys=%d" % (self.actions, self.buys)
        if self.coin:
            status += " Coins=%d" % self.coin
        if self.potions:
            status += " Potions=%d" % self.potions
        if self.specialcoins:
            status += " Special Coins=%d" % self.specialcoins
        prompt = "What to do (%s)?" % status
        return options, prompt

    ###########################################################################
    def turn(self):
        self.output("#" * 50)
        stats = "(%d points, %d cards)" % (self.getScore(), self.countCards())
        self.output("%s's Turn %s" % (self.name, stats))
        self.actionPhase()
        self.buyPhase()
        self.cleanupPhase()

    ###########################################################################
    def actionPhase(self):
        self.output("************ Action Phase ************")
        while(True):
            self.displayOverview()
            options, prompt = self.choiceSelection(phase='action')
            opt = self.userInput(options, prompt)
            self.perform_action(opt)
            if opt['action'] == 'quit':
                return

    ###########################################################################
    def buyPhase(self):
        self.output("************ Buy Phase ************")
        while(True):
            self.displayOverview()
            options, prompt = self.choiceSelection(phase='buy')
            opt = self.userInput(options, prompt)
            self.perform_action(opt)
            if opt['action'] == 'quit':
                return

    ###########################################################################
    def cleanupPhase(self):
        self.discardHand()
        self.pickUpHand()
        self.cleaned = True

    ###########################################################################
    def perform_action(self, opt):
        if opt['action'] == 'buy':
            self.buyCard(opt['card'])
        elif opt['action'] == 'event':
            self.performEvent(opt['card'])
        elif opt['action'] == 'reserve':
            self.callReserve(opt['card'].name)
        elif opt['action'] == 'coin':
            self.spendCoin()
        elif opt['action'] == 'play':
            self.playCard(opt['card'])
        elif opt['action'] == 'spend':
            self.playCard(opt['card'])
        elif opt['action'] == 'spendall':
            self.spendAllCards()
        elif opt['action'] == 'quit':
            return
        else:
            sys.stderr.write("ERROR: Unhandled action %s" % opt['action'])
            return
        self.is_start = False

    ###########################################################################
    def displayOverview(self):
        self.output('-' * 50)
        tknoutput = []
        for tkn in self.tokens:
            if self.tokens[tkn]:
                tknoutput.append("%s: %s" % (tkn, self.tokens[tkn]))
        if self.card_token:
            tknoutput.append("-1 Card")
        if self.coin_token:
            tknoutput.append("-1 Coin")
        if self.journey_token:
            tknoutput.append("Journey Faceup")
        else:
            tknoutput.append("Journey Facedown")
        self.output("| Tokens: %s" % "; ".join(tknoutput))
        if self.durationpile:
            self.output("| Duration: %s" % ", ".join([c.name for c in self.durationpile]))
        if self.reserve:
            self.output("| Reserve: %s" % ", ".join([c.name for c in self.reserve]))
        if self.hand:
            self.output("| Hand: %s" % ", ".join([c.name for c in self.hand]))
        else:
            self.output("| Hand: <EMPTY>")
        if self.played:
            self.output("| Played: %s" % ", ".join([c.name for c in self.played]))
        else:
            self.output("| Played: <NONE>")
        self.output('-' * 50)

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
        x += self.reserve
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
        self.cleaned = False
        self.is_start = True
        self.stats = {'gain': 0}
        for card in self.durationpile:
            self.output("Playing %s from duration pile" % card.name)
            card.duration(game=self.game, player=self)
            if not card.permanent:
                self.addCard(card, 'played')
                self.durationpile.remove(card)

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
        if not self.cleaned:
            self.cleanupPhase()
        self.newhandsize = 5

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
        if '+1 Action' in tkns:
            self.output("Gaining action from +1 Action token")
            self.actions += 1
        if '+1 Card' in tkns:
            c = self.pickupCard()
            self.output("Picked up %s from +1 Card token" % c.name)
        if '+1 Coin' in tkns:
            self.output("Gaining coin from +1 Coin token")
            self.coin += 1
        if '+1 Buy' in tkns:
            self.output("Gaining buy from +1 Buy token")
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
            self.output("-1 Card token reduces cards drawn")
            self.card_token = False
            modif = -1

        if card.isAction():
            for cd in self.played + self.durationpile:
                cd.hook_postAction(game=self.game, player=self)

        for i in range(card.cards + modif):
            self.pickupCard()
        try:
            card.special(game=self.game, player=self)
        except KeyboardInterrupt:   # pragma: no cover
            sys.stderr.write("\nFailed: %s\n" % self.messages)
            sys.exit(1)

    ###########################################################################
    def cardCost(self, card):
        assert(isinstance(card, (Card, CardPile)))
        cost = card.cost
        if '-Cost' in self.which_token(card.name):
            cost -= 2
        for c in self.hand + self.played + self.durationpile:
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
        if newcard:
            options = self.hook_gainCard(newcard)
        if not newcard:
            sys.stderr.write("ERROR: Getting from empty cardpile %s\n" % cardpile)
            return
        self.stats['gain'] += 1
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
        assert(isinstance(card, CardPile))
        if not self.buys:
            return
        newcard = self.gainCard(card)
        self.buys -= 1
        self.coin -= self.cardCost(newcard)
        self.output("Bought %s for %d coin" % (newcard.name, self.cardCost(newcard)))
        if 'Trashing' in self.which_token(card.name):
            self.output("Trashing token allows you to trash a card")
            self.plrTrashCard()
        self.hook_buyCard(newcard)
        newcard.hook_buyThisCard(game=self.game, player=self)
        self.hook_allPlayers_buyCard(newcard)

    ###########################################################################
    def hook_allPlayers_buyCard(self, card):
        for player in self.game.playerList():
            for cd in player.durationpile:
                cd.hook_allPlayers_buyCard(game=self.game, player=self, owner=player, card=card)

    ###########################################################################
    def hook_gainCard(self, card):
        """ Hook which is fired by a card being obtained by a player """
        assert(isinstance(card, Card))
        options = {}
        for c in self.hand:
            o = c.hook_gainCard(game=self.game, player=self, card=card)
            options.update(o)
        return options

    ###########################################################################
    def hook_gainThisCard(self, card):
        """ Hook which is fired by this card being obtained by a player """
        assert(isinstance(card, Card))
        card.hook_gainThisCard(game=self.game, player=self)

    ###########################################################################
    def hasDefense(self, attacker, verbose=True):
        assert(isinstance(attacker, Player))
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
        assert(isinstance(num, int))
        self.coin += num

    ###########################################################################
    def getActions(self):
        return self.actions

    ###########################################################################
    def addActions(self, num):
        assert(isinstance(num, int))
        self.actions += num

    ###########################################################################
    def getBuys(self):
        return self.buys

    ###########################################################################
    def addBuys(self, num):
        assert(isinstance(num, int))
        self.buys += num

    ###########################################################################
    def performEvent(self, event):
        assert(issubclass(event.__class__, EventPile))
        if not self.buys:
            self.output("Need a buy to perform an event")
            return False
        if self.coin < event.cost:
            self.output("Need %d coints to perform this event" % event.cost)
            return False
        self.buys -= 1
        self.coin -= event.cost
        self.output("Using event %s" % event.name)
        event.special(game=self.game, player=self)
        return True

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
            if coin is None:
                affordable.add(c)
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
        count = {}
        stacklist = (
            ('Discard', self.discardpile), ('Hand', self.hand),
            ('Reserve', self.reserve), ('Deck', self.deck),
            ('Played', self.played), ('Duration', self.durationpile))
        for name, stack in stacklist:
            count[name] = len(stack)
        total = sum([x for x in count.values()])
        total += self.secret_count
        return total

    ###########################################################################
    def typeSelector(self, types):
        if not types:
            return {'action': True, 'victory': True, 'treasure': True}
        _types = {'action': False, 'victory': False, 'treasure': False}
        _types.update(types)
        return _types

    ###########################################################################
    def attackVictims(self):
        """ Return list of other players who don't have defences """
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
    def plrTrashCard(self, num=1, anynum=False, printcost=False, force=False, exclude=[], cardsrc='hand'):
        """ Ask player to trash num cards
        """
        if anynum:
            prompt = "Trash any cards"
        else:
            prompt = "Trash %d cards" % num
        trash = self.cardSel(
            num=num, cardsrc=cardsrc, anynum=anynum, printcost=printcost,
            force=force, exclude=exclude, verbs=('Trash', 'Untrash'),
            prompt=prompt)
        for c in trash:
            self.trashCard(c)
        return trash

    ###########################################################################
    def plrGainCard(self, cost, modifier='less', types={}, recipient=None, force=False, destination='discard'):
        """ Gain a card up to cost coin
            if actiononly then gain only action cards
            if recipient defined then that player gets the card
        """
        if recipient is None:
            recipient = self
        prompt = "Gain a card "
        types = self.typeSelector(types)
        if modifier == 'less':
            if cost:
                prompt += "costing up to %d" % cost
            buyable = self.cardsUnder(cost, types=types)
        elif modifier == 'equal':
            if cost:
                prompt += "costing exactly %d" % cost
            buyable = self.cardsWorth(cost, types=types)
        buyable = [c for c in buyable if c.purchasable]
        cards = self.cardSel(
            cardsrc=buyable, recipient=recipient, verbs=('Get', 'Unget'),
            force=force, prompt=prompt)
        if cards:
            card = cards[0]
            recipient.output("Got a %s" % card.name)
            recipient.addCard(card.remove(), destination)
            return card

    ###########################################################################
    def plrPickCard(self, force=False, **kwargs):
        sel = self.cardSel(force=force, **kwargs)
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
