""" All the Player based stuff """
# pylint: disable=too-many-instance-attributes
import operator
import sys
from collections import defaultdict

from PlayArea import PlayArea
from Card import Card
from Option import Option
from CardPile import CardPile
from WayPile import WayPile
from EventPile import EventPile
from ProjectPile import ProjectPile


###############################################################################
###############################################################################
###############################################################################
class Player(object):
    def __init__(self, game, name, heirlooms=None):
        if heirlooms is None:
            heirlooms = []
        self.game = game
        self.name = name
        self.currcards = []
        game.output("Player %s is at the table" % name)
        self.score = {}
        self.coffer = 0
        self.villager = 0
        self.hadcards = []
        self.messages = []
        self.hand = PlayArea([])
        self.exilepile = PlayArea([])
        self.durationpile = PlayArea([])
        self.deck = PlayArea([])
        self.played = PlayArea([])
        self.discardpile = PlayArea([])
        self.debt = 0
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
        self.forbidden_to_buy = []
        self.played_events = PlayArea([])
        self.initial_Deck(heirlooms)
        self.initial_tokens()
        self.once = {}
        self.turn_number = 0
        self.stats = {'gained': [], 'bought': []}
        self.pickUpHand()
        self.secret_count = 0   # Hack to count cards that aren't anywhere normal
        self.end_of_game_cards = []
        self.phase = None
        self.states = []
        self.artifacts = []
        self.projects = []
        self.players = []
        self.stacklist = (
            ('Discard', self.discardpile), ('Hand', self.hand),
            ('Reserve', self.reserve), ('Deck', self.deck),
            ('Played', self.played), ('Duration', self.durationpile),
            ('Exile', self.exilepile)
        )

    ###########################################################################
    def initial_Deck(self, heirlooms=None):
        """ Provide the initial deck - cards don't come from the piles
            hence add them back
        """
        if heirlooms is None:
            heirlooms = []
        self.game['Copper'].pilesize += 7 - len(heirlooms)
        for _ in range(7 - len(heirlooms)):
            self.deck.add(self.game['Copper'].remove())
        for hl in heirlooms:
            self.deck.add(self.game[hl].remove())
        self.game['Estate'].pilesize += 3
        for _ in range(3):
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
    def find_cardpile(self, cname):
        dstcp = None
        for cp in self.game.cardpiles.values():
            if cp.name == cname:
                dstcp = cp
                break
        else:   # pragma: no cover
            assert dstcp is not None, "Couldn't find cardpile %s" % cname
        return dstcp

    ###########################################################################
    def replace_traveller(self, src, dst, **kwargs):
        """ For traveller cards replace the src card with a copy of the
        dst card """
        assert isinstance(src, Card)
        assert isinstance(dst, str)
        dstcp = self.find_cardpile(dst)

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
            self.replace_card(src, dst, destination='hand')

    ###########################################################################
    def replace_card(self, src, dst, **kwargs):
        # New card goes into hand as it is about to be discarded
        destination = kwargs['destination'] if 'destination' in kwargs else 'discard'

        dstcp = self.find_cardpile(dst)
        newcard = self.gainCard(cardpile=dstcp, destination=destination)
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
    def receive_hex(self, hx=None):
        if hx is None:
            hx = self.game.receive_hex()
        self.output("Received {} as a hex".format(hx))
        self.output("{}".format(hx.description(self)))
        for _ in range(hx.cards):
            self.pickupCard()
        self.actions += hx.actions
        self.buys += hx.buys
        self.coin += self.hook_spendValue(hx, actual=True)
        hx.special(game=self.game, player=self)
        self.game.discard_hex(hx)

    ###########################################################################
    def receive_boon(self, boon=None, discard=True):
        if boon is None:
            boon = self.game.receive_boon()
        self.output("Received {} as a boon".format(boon))
        self.output("{}".format(boon.description(self)))
        for _ in range(boon.cards):
            self.pickupCard()
        self.actions += boon.actions
        self.buys += boon.buys
        self.coin += self.hook_spendValue(boon, actual=True)
        boon.special(game=self.game, player=self)
        if discard:
            self.game.discard_boon(boon)
        return boon

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
        assert isinstance(pilename, str)
        self.tokens[token] = pilename

    ###########################################################################
    def which_token(self, pilename):
        """ Return which token(s) are on a cardstack """
        assert isinstance(pilename, str)
        onstack = []
        for tk in self.tokens:
            if self.tokens[tk] == pilename:
                onstack.append(tk)
        return onstack

    ###########################################################################
    def call_reserve(self, card):
        if isinstance(card, str):
            card = self.inReserve(card)
            if not card:
                return None
        assert isinstance(card, Card)
        self.output("Calling %s from Reserve" % card.name)
        self.currcards.append(card)
        card.hook_call_reserve(game=self.game, player=self)
        self.currcards.pop()
        self.reserve.remove(card)
        self.addCard(card, 'played')
        return card

    ###########################################################################
    def inReserve(self, cardname):
        """ Return named card if cardname is in reserve """
        assert isinstance(cardname, str)
        for card in self.reserve:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inHand(self, cardname):
        """ Return named card if cardname is in hand """
        assert isinstance(cardname, str)

        for card in self.hand:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def revealCard(self, card):
        self.game.output("{} reveals {}".format(self.name, card.name))
        card.hook_revealThisCard(game=self.game, player=self)

    ###########################################################################
    def inDuration(self, cardname):
        """ Return named card if cardname is in the duration pile """
        assert isinstance(cardname, str)

        for card in self.durationpile:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def unexile(self, card):
        """ Remove card from exile pile into discard pile """
        self.exilepile.remove(card)
        self.discardpile.add(card)

    ###########################################################################
    def in_exile(self, cardname):
        """ Return named card if cardname is in the exile pile """
        assert isinstance(cardname, str)

        for card in self.exilepile:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inDiscard(self, cardname):
        """ Return named card if cardname is in the discard pile """
        assert isinstance(cardname, str)

        for card in self.discardpile:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inPlayed(self, cardname):
        """ Return named card if cardname is in the played pile """
        assert isinstance(cardname, str)

        for card in self.played:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def inDeck(self, cardname):
        """ Return named card if cardname is in the deck pile """
        assert isinstance(cardname, str)

        for card in self.deck:
            if card.name == cardname:
                return card
        return None

    ###########################################################################
    def trashCard(self, card):
        """ Take a card out of the game """
        assert isinstance(card, Card)
        trashopts = {}
        rc = card.hook_trashThisCard(game=self.game, player=self)
        if rc:
            trashopts.update(rc)
        for cd in self.hand + self.game.landmarks + self.played:
            rc = cd.hook_trashCard(game=self.game, player=self, card=card)
            if rc:
                trashopts.update(rc)
        if 'trash' in trashopts and not trashopts['trash']:
            return
        self.game.trashpile.add(card)
        if card in self.played:
            self.played.remove(card)
        elif card in self.hand:
            self.hand.remove(card)

    ###########################################################################
    def set_exile(self, *cards):
        """ This is mostly used for testing """
        self.exilepile.empty()
        for c in cards:
            self.exilepile.add(self.game[c].remove())

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
        self.shuffleDiscard()
        while self.discardpile:
            self.addCard(self.discardpile.topcard(), 'deck')

    ###########################################################################
    def pickupCards(self, num, verbose=True, verb='Picked up'):
        cards = []
        for _ in range(num):
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
        assert isinstance(card, Card)
        self.addCard(card, 'hand')
        if verbose:
            self.output("%s %s" % (verb, card.name))
        return card

    ###########################################################################
    def shuffleDiscard(self):
        self.output("Shuffling Pile of %d cards" % len(self.discardpile))
        for card in self.projects:
            if hasattr(card, 'hook_preShuffle'):
                card.hook_preShuffle(game=self.game, player=self)
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
    def gainVillager(self, num=1):
        """ Gain a number of villager """
        self.villager += num

    ###########################################################################
    def gainCoffer(self, num=1):
        """ Gain a number of coffer """
        self.coffer += num

    ###########################################################################
    def addCard(self, card, pile='discard'):
        if not card:   # pragma: no cover
            return
        assert isinstance(card, Card)
        assert pile in ('discard', 'hand', 'topdeck', 'deck', 'played', 'duration', 'reserve')
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
    def discardCard(self, card, source=None, hook=True):
        assert isinstance(card, Card)
        if card in self.hand:
            self.hand.remove(card)
        self.addCard(card, 'discard')
        if hook:
            self.hook_discardThisCard(card, source)

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
        # Activate hooks first so they can still access contents of the
        # players hand etc. before they get discarded
        for card in self.hand:
            self.hook_discardThisCard(card, 'hand')
        for card in self.played:
            self.hook_discardThisCard(card, 'played')
        while self.hand:
            card = self.hand.topcard()
            self.discardCard(card, 'hand', hook=False)
        while self.played:
            card = self.played.topcard()
            self.discardCard(card, 'played', hook=False)

    ###########################################################################
    def playable_selection(self, index):
        options = []
        playable = [c for c in self.hand if c.playable and c.isAction()]
        if self.villager:
            o = Option(selector='1', verb='Spend Villager (1 action)', card=None, action='villager')
            options.append(o)

        for p in playable:
            sel = chr(ord('a') + index)
            details = p.get_cardtype_repr()
            o = Option(verb="Play", selector=sel, name=p.name, desc=p.description(self).strip(), action='play', card=p, details=details)
            notes = ""
            for tkn in self.which_token(p.name):
                notes += "[Tkn: %s]" % tkn
            o['notes'] = notes
            options.append(o)
            index += 1
        return options, index

    ###########################################################################
    def night_selection(self, index):
        options = []
        nights = [c for c in self.hand if c.isNight()]
        if nights:
            for n in nights:
                sel = chr(ord('a') + index)
                details = n.get_cardtype_repr()
                o = Option(verb="Play", selector=sel, name=n.name, details=details, card=n, action='play', desc=n.description(self))
                options.append(o)
                index += 1
        return options, index

    ###########################################################################
    def spendable_selection(self):
        options = []
        spendable = [c for c in self.hand if c.isTreasure()]
        totcoin = sum([self.hook_spendValue(c) for c in spendable])
        numpots = sum([1 for c in spendable if c.name == 'Potion'])
        potstr = ", %d potions" % numpots if numpots else ""
        details = '%d coin%s' % (totcoin, potstr)
        if spendable:
            o = Option(selector='1', verb='Spend all treasures', details=details, card=None, action='spendall')
            options.append(o)

        if self.coffer:
            o = Option(selector='2', verb='Spend Coffer (1 coin)', card=None, action='coffer')
            options.append(o)

        if self.debt and self.coin:
            o = Option(selector='3', verb='Payback Debt', card=None, action='payback')
            options.append(o)

        index = 4
        for s in spendable:
            tp = '%d coin; %s' % (self.hook_spendValue(s), s.get_cardtype_repr())
            o = Option(selector=str(index), name=s.name, details=tp, verb='Spend', card=s, action='spend', desc=s.description(self))
            options.append(o)
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
    def reserve_selection(self, index):
        whens = self.getWhens()
        options = []
        for card in self.reserve:
            if not card.callable:
                continue
            if card.when not in whens:
                continue
            index += 1
            sel = chr(ord('a') + index)
            details = card.get_cardtype_repr()
            o = Option(selector=sel, name=card.name, verb='Call', details=details, card=card, action='reserve', desc=card.description(self))
            options.append(o)

        return options, index

    ###########################################################################
    def landmark_selection(self, index):
        options = []
        for lm in self.game.landmarks.values():
            o = Option(selector='-', desc=lm.description(self), name=lm.name, card=lm, action=None, details="Landmark")
            options.append(o)

        return options, index

    ###########################################################################
    def project_selection(self, index):
        if not self.game.projects:
            return None, index
        # Can only have two projects
        if len(self.projects) == 2:
            return None, index
        options = []
        for op in self.game.projects.values():
            index += 1
            if (op.cost <= self.coin and self.buys) and (op not in self.projects):
                sel = chr(ord('a') + index)
                action = 'project'
            else:
                sel = '-'
                action = None
            details = "Project; %s" % self.coststr(op)
            o = Option(selector=sel, verb='Buy', desc=op.description(self), name=op.name, details=details, card=op, action=action)
            options.append(o)

        return options, index

    ###########################################################################
    def event_selection(self, index):
        options = []
        for op in self.game.events.values():
            index += 1
            if op.cost <= self.coin and self.buys:
                sel = chr(ord('a') + index)
                action = 'event'
            else:
                sel = '-'
                action = None
            details = "Event; %s" % self.coststr(op)
            o = Option(selector=sel, verb='Use', desc=op.description(self), name=op.name, details=details, card=op, action=action)
            options.append(o)

        return options, index

    ###########################################################################
    def getAllPurchasable(self):
        """ Return all potentially purchasable cards """
        all_cards = PlayArea([])
        for c in self.game.cardTypes():
            if not c.purchasable:
                continue
            all_cards.add(c)
        all_cards.sort(key=self.cardCost)
        all_cards.sort(key=lambda c: c.basecard)
        return all_cards

    ###########################################################################
    def buyable_selection(self, index):
        options = []
        all_cards = self.getAllPurchasable()
        buyable = self.cardsUnder(coin=self.coin, potions=self.potions)
        for card in all_cards:
            if not self.hook_allowedToBuy(card):
                if card in buyable:
                    buyable.remove(card)
            sel = chr(ord('a') + index)
            if not self.debt and self.buys and card in buyable and card not in self.forbidden_to_buy:
                action = 'buy'
                verb = 'Buy'
            else:
                sel = '-'
                verb = ''
                action = None
            details = [self.coststr(card)]
            if card.embargo_level:
                details.append("Embargo %d" % card.embargo_level)
            if card.getVP():
                details.append("Gathered %d VP" % card.getVP())
            details.append(card.get_cardtype_repr())
            details.append('%d left' % card.pilesize)
            for tkn in self.which_token(card.name):
                details.append("[Tkn: %s]" % tkn)
            o = Option(
                selector=sel, verb=verb, desc=card.description(self),
                name=card.name, details="; ".join(details), card=card,
                action=action
            )
            options.append(o)
            index += 1
        return options, index

    ###########################################################################
    def choice_selection(self):
        index = 0
        o = Option(selector='0', verb='End Phase', card=None, action='quit')
        options = [o]

        if self.phase == 'action':
            if self.actions or self.villager:
                op, index = self.playable_selection(index)
                options.extend(op)

        if self.phase == 'buy':
            op = self.spendable_selection()
            options.extend(op)
            op, index = self.buyable_selection(index)
            options.extend(op)
            op, index = self.event_selection(index)
            options.extend(op)
            op, index = self.project_selection(index)
            if op:
                options.extend(op)

        if self.phase == 'night':
            op, index = self.night_selection(index)
            options.extend(op)

        if self.reserveSize():
            op, index = self.reserve_selection(index)
            options.extend(op)

        op, index = self.landmark_selection(index)
        options.extend(op)

        status = "Actions=%d Buys=%d" % (self.actions, self.buys)
        if self.coin:
            status += " Coins=%d" % self.coin
        if self.debt:
            status += " Debt=%s" % self.debt
        if self.potions:
            status += " Potion"
        if self.coffer:
            status += " Coffer=%d" % self.coffer
        if self.villager:
            status += " Villager=%d" % self.villager
        prompt = "What to do (%s)?" % status
        return options, prompt

    ###########################################################################
    def turn(self):
        self.turn_number += 1
        self.output("%s Turn %d %s" % ("#" * 20, self.turn_number, "#" * 20))
        stats = "(%d points, %d cards)" % (self.getScore(), self.countCards())
        self.output("%s's Turn %s" % (self.name, stats))
        self.action_phase()
        self.buy_phase()
        self.night_phase()
        self.cleanup_phase()

    ###########################################################################
    def night_phase(self):
        nights = [c for c in self.hand if c.isNight()]
        if not nights:
            return
        self.output("************ Night Phase ************")
        self.phase = 'night'
        while True:
            self.displayOverview()
            options, prompt = self.choice_selection()
            opt = self.userInput(options, prompt)
            self.perform_action(opt)
            if opt['action'] == 'quit':
                return

    ###########################################################################
    def action_phase(self):
        self.output("************ Action Phase ************")
        self.phase = 'action'
        while True:
            self.displayOverview()
            options, prompt = self.choice_selection()
            opt = self.userInput(options, prompt)
            self.perform_action(opt)
            if opt['action'] == 'quit':
                return

    ###########################################################################
    def buy_phase(self):
        self.output("************ Buy Phase ************")
        self.phase = 'buy'
        self.hook_preBuy()
        while True:
            self.displayOverview()
            options, prompt = self.choice_selection()
            opt = self.userInput(options, prompt)
            self.perform_action(opt)
            if opt['action'] == 'quit':
                break
        self.hook_endBuyPhase()

    ###########################################################################
    def hook_endBuyPhase(self):
        for card in self.projects:
            card.hook_endBuyPhase(game=self.game, player=self)

    ###########################################################################
    def cleanup_phase(self):
        # Save the cards we had so that the hook_end_turn has something to apply against
        self.hadcards = self.played + self.reserve + self.played_events + self.game.landmarks + self.durationpile
        self.phase = 'cleanup'
        self.game.cleanup_boons()
        self.game.cleanup_hexes()
        for card in self.played + self.reserve + self.artifacts:
            card.hook_cleanup(self.game, self)
        self.discardHand()
        self.pickUpHand()
        self.cleaned = True

    ###########################################################################
    def payback(self):
        pb = min(self.coin, self.debt)
        self.output("Paying back %d debt" % pb)
        self.coin -= pb
        self.debt -= pb

    ###########################################################################
    def perform_action(self, opt):
        if opt['action'] == 'buy':
            self.buyCard(opt['card'])
        elif opt['action'] == 'event':
            self.performEvent(opt['card'])
        elif opt['action'] == 'project':
            self.buyProject(opt['card'])
        elif opt['action'] == 'reserve':
            self.call_reserve(opt['card'])
        elif opt['action'] == 'coffer':
            self.spendCoffer()
        elif opt['action'] == 'villager':
            self.spendVillager()
        elif opt['action'] == 'play':
            self.playCard(opt['card'])
        elif opt['action'] == 'spend':
            self.playCard(opt['card'])
        elif opt['action'] == 'payback':
            self.payback()
        elif opt['action'] == 'spendall':
            self.spendAllCards()
        elif opt['action'] == 'quit':
            return
        else:   # pragma: no cover
            sys.stderr.write("ERROR: Unhandled action %s" % opt['action'])
            sys.exit(1)
        self.is_start = False

    ###########################################################################
    def displayOverview(self):  # pylint: disable=too-many-branches
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
        if self.projects:
            self.output("| Project: %s" % ", ".join([p.name for p in self.projects]))
        if self.reserve:
            self.output("| Reserve: %s" % ", ".join([c.name for c in self.reserve]))
        if self.hand:
            self.output("| Hand: %s" % ", ".join([c.name for c in self.hand]))
        else:
            self.output("| Hand: <EMPTY>")
        if self.artifacts:
            self.output("| Artifacts: %s" % ", ".join([c.name for c in self.artifacts]))
        if self.exilepile:
            self.output("| Exile: %s" % ", ".join([c.name for c in self.exilepile]))
        if self.played:
            self.output("| Played: %s" % ", ".join([c.name for c in self.played]))
        else:
            self.output("| Played: <NONE>")
        self.output("| {} cards in discard pile".format(self.discardSize()))
        self.output('-' * 50)

    ###########################################################################
    def addScore(self, reason, points=1):
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
        x += self.exilepile
        return x

    ###########################################################################
    def getScoreDetails(self, verbose=False):
        scr = {}
        for c in self.allCards():
            scr[c.name] = scr.get(c.name, 0) + c.victory
            scr[c.name] = scr.get(c.name, 0) + c.special_score(self.game, self)
        for s in self.states:
            scr[s.name] = scr.get(s.name, 0) + s.victory
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
    def hook_preBuy(self):
        """ Hook that fires off before the buy phase """
        for card in list(self.game.landmarks.values()) + self.states + self.artifacts:
            card.hook_preBuy(game=self.game, player=self)

    ###########################################################################
    def hook_allowedToBuy(self, card):
        """ Hook to check if you are allowed to buy a card """
        return card.hook_allowedToBuy(game=self.game, player=self)

    ###########################################################################
    def hook_buyCard(self, card):
        """ Hook for after purchasing a card """
        for c in self.played + self.reserve + self.game.landmarks:
            c.hook_buyCard(game=self.game, player=self, card=card)

    ###########################################################################
    def startTurn(self):
        self.phase = 'start'
        self.played.empty()
        self.buys = 1
        self.actions = 1
        self.coin = 0
        self.potions = 0
        self.cleaned = False
        self.is_start = True
        self.stats = {'gained': [], 'bought': []}
        self.displayOverview()
        self.hook_startTurn()
        for card in self.durationpile:
            self.output("Playing %s from duration pile" % card.name)
            self.currcards.append(card)
            card.duration(game=self.game, player=self)
            self.currcards.pop()
            if not card.permanent:
                self.addCard(card, 'played')
                self.durationpile.remove(card)

    ###########################################################################
    def hook_startTurn(self):
        for c in self.hand + self.states + self.projects + self.artifacts:
            c.hook_startTurn(self.game, self)

    ###########################################################################
    def spendCoffer(self):
        if self.coffer <= 0:
            return
        self.coffer -= 1
        self.coin += 1
        self.output("Spent a coffer")

    ###########################################################################
    def spendVillager(self):
        if self.villager <= 0:
            return
        self.villager -= 1
        self.actions += 1
        self.output("Spent a villager")

    ###########################################################################
    def exile_card(self, card):
        """ Send a card to the exile pile """
        self.exilepile.add(card)

    ###########################################################################
    def end_turn(self):
        if not self.cleaned:
            self.cleanup_phase()
        for card in self.hadcards:
            self.currcards.append(card)
            card.hook_end_turn(game=self.game, player=self)
            self.currcards.pop()
        self.newhandsize = 5
        self.played_events = PlayArea([])
        self.messages = []
        self.forbidden_to_buy = []
        self.once = {}
        self.phase = None
        self.hadcards = []

    ###########################################################################
    def hook_discardThisCard(self, card, source=None):
        """ A card has been discarded """
        self.currcards.append(card)
        card.hook_discardThisCard(game=self.game, player=self, source=source)
        self.currcards.pop()

    ###########################################################################
    def hook_spendValue(self, card, actual=False):
        """ How much do you get for spending the card
            If actual is True then we are spending the coin rather than
            just working out what we would get for spending it
        """
        val = card.hook_coinvalue(game=self.game, player=self)
        for c in self.played:
            val += c.hook_spendValue(game=self.game, player=self, card=card)
        for s in self.states:
            val += s.hook_spendValue(game=self.game, player=self, card=card)
        if val and self.coin_token:
            val -= 1
            if actual:
                self.coin_token = False
        return val

    ###########################################################################
    def spendAllCards(self):
        for card in self.hand[:]:
            if card.isTreasure():
                self.playCard(card)

    ###########################################################################
    def playCard_Tokens(self, card):
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

    ###########################################################################
    def hook_allPlayers_preAction(self, card):
        options = {}
        for player in self.game.player_list():
            for crd in player.durationpile:
                ans = crd.hook_allPlayers_preAction(game=self.game, player=self, owner=player, card=card)
                if ans:
                    options.update(ans)
        return options

    ###########################################################################
    def playCard(self, card, discard=True, costAction=True, postActionHook=True):
        options = {'skip_card': False}
        if card not in self.hand and discard:
            self.output("{} is no longer available".format(card.name))
            return
        self.output("Playing %s" % card.name)
        self.currcards.append(card)
        if card.isAction():
            options.update(self.hook_allPlayers_preAction(card))
        if card.isAction() and costAction and self.phase != 'night':
            self.actions -= 1
        if self.actions < 0:    # pragma: no cover
            self.actions = 0
            self.currcards.pop()
            self.output("Not enough actions")
            return
        self.playCard_Tokens(card)
        if discard:
            if card.isDuration():
                self.addCard(card, 'duration')
            elif card.isReserve():
                self.addCard(card, 'reserve')
            else:
                self.addCard(card, 'played')
            self.hand.remove(card)

        way = None
        if not options['skip_card']:
            if self.game.ways and card.isAction():
                way = self.select_ways()
            if way:
                self.perform_way(way)
            else:
                self.card_benefits(card)
        self.currcards.pop()
        if postActionHook and card.isAction():
            for cd in self.played + self.durationpile + self.projects:
                if hasattr(cd, 'hook_postAction'):
                    cd.hook_postAction(game=self.game, player=self, card=card)

    ###########################################################################
    def select_ways(self):
        """ Select a way to perform """
        options = [("Do not use a way", None)]
        for way in self.game.ways.values():
            options.append(("{}: {}".format(way.name, way.description(self)), way))
        ans = self.plrChooseOptions("Select a way to perform", *options)
        return ans

    ###########################################################################
    def perform_way(self, way):
        """ Perform a way """
        self.card_benefits(way)

    ###########################################################################
    def card_benefits(self, card):
        self.actions += card.actions
        self.coin += self.hook_spendValue(card, actual=True)
        self.buys += card.buys
        self.potions += card.potion

        modif = 0
        if self.card_token and card.cards:
            self.output("-1 Card token reduces cards drawn")
            self.card_token = False
            modif = -1

        for _ in range(card.cards + modif):
            self.pickupCard()

        if self.phase == 'night':
            card.night(game=self.game, player=self)
        else:
            card.special(game=self.game, player=self)

    ###########################################################################
    def cardCost(self, card):
        assert isinstance(card, (Card, CardPile, EventPile, ProjectPile, WayPile))
        cost = card.cost
        if '-Cost' in self.which_token(card.name):
            cost -= 2
        for c in self.hand + self.played + self.durationpile + self.states + self.projects:
            cost += c.hook_cardCost(game=self.game, player=self, card=card)
        cost += card.hook_thisCardCost(game=self.game, player=self)
        return max(0, cost)

    ###########################################################################
    def gainCard(self, cardpile=None, destination='discard', newcard=None, callhook=True):
        """ Add a new card to the players set of cards from a cardpile """
        # Options:
        #   dontadd: True - adding card handled elsewhere
        #   replace: <newcard> - Replace the gained card with <newcard>
        #   destination: <dest> - Move the new card to <dest> rather than discardpile
        #   trash: True - trash the new card
        #   shuffle: True - shuffle the deck after gaining new card
        options = {}
        if not newcard:
            if isinstance(cardpile, str):
                newcard = self.game[cardpile].remove()
            else:
                newcard = cardpile.remove()
        if not newcard:
            self.output("No more %s" % cardpile)
            return None
        if callhook:
            rc = self.hook_gainCard(newcard)
            if rc:
                options.update(rc)
        if callhook:
            rc = newcard.hook_gainThisCard(game=self.game, player=self)
            if rc:
                options.update(rc)

        # check for un-exiling
        if self.in_exile(newcard.name):
            self.check_unexile(newcard.name)

        # Replace is to gain a different card
        if 'replace' in options:
            self.game[newcard.name].add()
            newcard = self.game[options['replace']].remove()
        self.stats['gained'].append(newcard)
        if options.get('destination'):
            destination = options['destination']
        self.hook_allPlayers_gainCard(newcard)
        if options.get('trash', False):
            self.trashCard(newcard)
            return newcard
        if not options.get('dontadd', False):
            self.addCard(newcard, destination)
        if options.get('shuffle', False):
            self.deck.shuffle()
        return newcard

    ###########################################################################
    def check_unexile(self, cardname):
        """ Give players option to un-exile card """
        num = sum([1 for _ in self.exilepile if _.name == cardname])
        choices = [
            ("Un-exile {} x {}".format(num, cardname), True),
            ("Don't un-exile {}".format(cardname), False)
        ]
        unex = self.plrChooseOptions(
            "Un-exile {}".format(cardname), *choices
        )
        if unex:
            for card in self.exilepile[:]:
                if card.name == cardname:
                    self.unexile(card)

    ###########################################################################
    def overpay(self, card):
        options = []
        for i in range(self.coin+1):
            options.append(("Spend %d more" % i, i))
        ans = self.plrChooseOptions(
            "How much do you wish to overpay?",
            *options
            )
        card.hook_overpay(game=self.game, player=self, amount=ans)
        self.coin -= ans

    ###########################################################################
    def buyCard(self, card):
        assert isinstance(card, CardPile)
        if not self.buys:   # pragma: no cover
            return
        if self.debt != 0:
            self.output("Must pay off debt first")
            return
        self.buys -= 1
        cost = self.cardCost(card)
        if card.isDebt():
            self.debt += card.debtcost
        self.coin -= cost
        if card.overpay and self.coin:
            self.overpay(card)
        newcard = self.gainCard(card)
        if card.embargo_level:
            for _ in range(card.embargo_level):
                self.gainCard('Curse')
                self.output("Gained a Curse from embargo")
        self.stats['bought'].append(newcard)
        self.output("Bought %s for %d coin" % (newcard.name, cost))
        if 'Trashing' in self.which_token(card.name):
            self.output("Trashing token allows you to trash a card")
            self.plrTrashCard()
        self.hook_buyCard(newcard)
        newcard.hook_buyThisCard(game=self.game, player=self)
        self.hook_allPlayers_buyCard(newcard)

    ###########################################################################
    def hook_allPlayers_buyCard(self, card):
        for player in self.game.player_list():
            for crd in player.durationpile:
                crd.hook_allPlayers_buyCard(game=self.game, player=self, owner=player, card=card)
        for crd in self.game.landmarks.values():
            crd.hook_allPlayers_buyCard(game=self.game, player=self, owner=self, card=card)

    ###########################################################################
    def hook_allPlayers_gainCard(self, card):
        for player in self.game.player_list():
            for crd in player.hand + player.projects:
                crd.hook_allPlayers_gainCard(game=self.game, player=self, owner=player, card=card)

    ###########################################################################
    def hook_gainCard(self, card):
        """ Hook which is fired by a card being obtained by a player """
        assert isinstance(card, Card)
        options = {}
        for c in self.hand + self.played + self.durationpile + self.reserve + self.game.landmarks + self.projects:
            self.currcards.append(c)
            o = c.hook_gainCard(game=self.game, player=self, card=card)
            self.currcards.pop()
            if o:
                options.update(o)
        return options

    ###########################################################################
    def hasDefense(self, attacker, verbose=True):
        assert isinstance(attacker, Player)
        for c in self.hand:
            c.hook_underAttack(game=self.game, player=self, attacker=attacker)
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
    def getCoffer(self):
        return self.coffer

    ###########################################################################
    def setCoffer(self, num=0):
        self.coffer = num

    ###########################################################################
    def getVillager(self):
        return self.villager

    ###########################################################################
    def addCoin(self, num=1):
        assert isinstance(num, int)
        self.coin += num

    ###########################################################################
    def setCoin(self, num=1):
        assert isinstance(num, int)
        self.coin = num

    ###########################################################################
    def getActions(self):
        return self.actions

    ###########################################################################
    def addActions(self, num=1):
        assert isinstance(num, int)
        self.actions += num

    ###########################################################################
    def getBuys(self):
        return self.buys

    ###########################################################################
    def addBuys(self, num=1):
        assert isinstance(num, int)
        self.buys += num

    ###########################################################################
    def setBuys(self, num=1):
        assert isinstance(num, int)
        self.buys = num

    ###########################################################################
    def gainPrize(self):
        prizes = [self.game[c] for c in self.game.getPrizes()]
        available = [cp for cp in prizes if not cp.isEmpty()]
        if available:
            self.output("Gain a prize")
            card = self.cardSel(cardsrc=available)
            self.addCard(card[0].remove())
        else:
            self.output("No prizes available")

    ###########################################################################
    def __str__(self):
        return "<Player %s>" % self.name

    ###########################################################################
    def buyProject(self, project):
        assert issubclass(project.__class__, ProjectPile)
        if not self.buys:
            self.output("Need a buy to buy a project")
            return False
        if self.debt != 0:
            self.output("Must pay off debt first")
            return False
        if self.coin < project.cost:
            self.output("Need %d coints to buy this project" % project.cost)
            return False
        self.buys -= 1
        self.coin -= project.cost
        self.debt += project.debtcost
        self.buys += project.buys
        self.assign_project(project.name)
        return True

    ###########################################################################
    def performEvent(self, event):
        assert issubclass(event.__class__, EventPile)
        if not self.buys:
            self.output("Need a buy to perform an event")
            return False
        if self.debt != 0:
            self.output("Must pay off debt first")
        if self.coin < event.cost:
            self.output("Need %d coints to perform this event" % event.cost)
            return False
        self.buys -= 1
        self.coin -= event.cost
        self.debt += event.debtcost
        self.buys += event.buys
        self.output("Using event %s" % event.name)
        self.currcards.append(event)
        event.special(game=self.game, player=self)
        self.currcards.pop()
        self.played_events.add(event)
        return True

    ###########################################################################
    def select_by_type(self, card, types):
        if card.isAction() and not types['action']:
            return False
        if card.isVictory() and not types['victory']:
            return False
        if card.isTreasure() and not types['treasure']:
            return False
        if card.isNight() and not types['night']:
            return False
        return True

    ###########################################################################
    def cardsAffordable(self, oper, coin, potions, types):
        """Return the list of cards for under cost """
        affordable = PlayArea([])
        for c in self.game.cardTypes():
            if not c.pilesize:
                continue
            cost = self.cardCost(c)
            if not self.select_by_type(c, types):
                continue
            if not c.purchasable:
                continue
            if coin is None:
                affordable.add(c)
                continue
            if c.debtcost and not c.cost:
                affordable.add(c)
                continue
            if oper(cost, coin) and oper(c.potcost, potions):
                affordable.add(c)
                continue
        affordable.sort(key=self.cardCost)
        affordable.sort(key=lambda c: c.basecard)
        return affordable

    ###########################################################################
    def cardsUnder(self, coin, potions=0, types=None):
        """Return the list of cards for under cost """
        if types is None:
            types = {}
        types = self.typeSelector(types)
        return self.cardsAffordable(operator.le, coin, potions, types)

    ###########################################################################
    def cardsWorth(self, coin, potions=0, types=None):
        """Return the list of cards that are exactly cost """
        if types is None:
            types = {}
        types = self.typeSelector(types)
        return self.cardsAffordable(operator.eq, coin, potions, types)

    ###########################################################################
    def getCards(self):
        """ Return a list of all teh cards owned """
        cards = defaultdict(int)
        for _, stack in self.stacklist:
            for card in stack:
                cards[card.name] += 1
        return cards

    ###########################################################################
    def countCards(self):
        count = {}
        for name, stack in self.stacklist:
            count[name] = len(stack)
        total = sum(count.values())
        total += self.secret_count
        return total

    ###########################################################################
    def typeSelector(self, types=None):
        if types is None:
            types = {}
        assert set(types.keys()) <= set(['action', 'victory', 'treasure', 'night'])
        if not types:
            return {'action': True, 'victory': True, 'treasure': True, 'night': True}
        _types = {'action': False, 'victory': False, 'treasure': False, 'night': False}
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
        cost = []
        cost.append("%d Coins" % self.cardCost(card))
        if card.debtcost:
            cost.append("%d Debt" % card.debtcost)
        if card.potcost:
            cost.append("Potion")
        if card.overpay:
            cost.append("Overpay")
        cststr = ", ".join(cost)
        return cststr.strip()

    ###########################################################################
    def plrTrashCard(self, num=1, anynum=False, printcost=False, force=False, exclude=None, cardsrc='hand', **kwargs):
        """ Ask player to trash num cards """
        if exclude is None:
            exclude = []
        if 'prompt' not in kwargs:
            if anynum:
                kwargs['prompt'] = "Trash any cards"
            else:
                kwargs['prompt'] = "Trash %d cards" % num
        if len(cardsrc) == 0:
            return None
        trash = self.cardSel(
            num=num, cardsrc=cardsrc, anynum=anynum, printcost=printcost,
            force=force, exclude=exclude, verbs=('Trash', 'Untrash'), **kwargs)
        for c in trash:
            self.trashCard(c)
        return trash

    ###########################################################################
    def plrGainCard(self, cost, modifier='less', types=None, recipient=None, force=False, destination='discard', **kwargs):
        """ Gain a card up to cost coin
            if recipient defined then that player gets the card """
        if types is None:
            types = {}
        assert modifier in ('less', 'equal')
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
        buyable = [c for c in buyable if not c.debtcost]
        if 'prompt' not in kwargs:
            kwargs['prompt'] = prompt
        cards = self.cardSel(
            cardsrc=buyable, recipient=recipient, verbs=('Get', 'Unget'),
            force=force, **kwargs)
        if cards:
            cardpile = cards[0]
            newcard = recipient.gainCard(cardpile, destination)
            recipient.output("Got a %s" % newcard.name)
            return newcard
        return None

    ###########################################################################
    def plrPickCard(self, force=False, **kwargs):
        sel = self.cardSel(force=force, **kwargs)
        return sel[0]

    ###########################################################################
    def has_state(self, state):
        return state in [_.name for _ in self.states]

    ###########################################################################
    def has_artifact(self, artifact):
        return artifact in [_.name for _ in self.artifacts]

    ###########################################################################
    def assign_state(self, state):
        assert isinstance(state, str)
        statecard = self.game.states[state]

        if statecard.unique_state:
            for pl in self.game.player_list():
                for st in pl.states[:]:
                    if st.name == state:
                        pl.states.remove(st)
                        break
        self.states.append(statecard)

    ###########################################################################
    def assign_artifact(self, artifact):
        assert isinstance(artifact, str)
        artifactcard = self.game.artifacts[artifact]
        # Remove artifact from whoever currently has it
        for pl in self.game.player_list():
            for st in pl.artifacts[:]:
                if st.name == artifact and self != pl:
                    pl.output("{} took your {}".format(self.name, artifact))
                    pl.artifacts.remove(st)
                    break
        # If we already have it don't get it again
        if artifactcard not in self.artifacts:
            self.artifacts.append(artifactcard)

    ###########################################################################
    def assign_project(self, project):
        assert isinstance(project, str)
        projectcard = self.game.projects[project]
        if len(self.projects) == 2:
            self.output("Can't have more than two projects")
            return False
        if project in [_.name for _ in self.projects]:
            self.output("Already have project {}".format(project))
            return False
        self.projects.append(projectcard)
        return True

    ###########################################################################
    def remove_state(self, state):
        if isinstance(state, str):
            name = state
        else:
            name = state.name
        self.states.remove([_ for _ in self.states if _.name == name][0])

    ###########################################################################
    def remove_artifact(self, artifact):
        if isinstance(artifact, str):
            name = artifact
        else:
            name = artifact.name
        self.artifacts.remove([_ for _ in self.artifacts if _.name == name][0])

    ###########################################################################
    def plrDiscardCards(self, num=1, anynum=False, **kwargs):
        """ Get the player to discard exactly num cards """
        if 'prompt' not in kwargs:
            if anynum:
                kwargs['prompt'] = "Discard any number of cards"
            else:
                kwargs['prompt'] = "Discard %d cards" % num
        discard = self.cardSel(
            num=num, anynum=anynum, verbs=('Discard', 'Undiscard'), **kwargs)
        for c in discard:
            self.output("Discarding %s" % c.name)
            self.discardCard(c)
        return discard

    ###########################################################################
    def plrDiscardDownTo(self, num):
        """ Get the player to discard down to num cards in their hand """
        numtogo = len(self.hand) - num
        if numtogo <= 0:
            return
        self.plrDiscardCards(numtogo, force=True)

    ###########################################################################
    def gameOver(self):
        """ Game is over - do anything special required """
        for card in self.end_of_game_cards + list(self.game.landmarks.values()):
            card.hook_end_of_game(game=self.game, player=self)

    ###########################################################################
    def output(self, msg, end=None):
        raise NotImplementedError

    ###########################################################################
    def plrChooseOptions(self, prompt, *choices):
        raise NotImplementedError

    ###########################################################################
    def userInput(self, options, prompt):
        raise NotImplementedError

    ###########################################################################
    def cardSel(self, num=1, **kwargs):
        raise NotImplementedError

# EOF
