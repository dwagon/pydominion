from Card import Card


class Card_Secretchamber(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'intrigue'
        self.desc = "Discard any number of cards; +1 gold per card discarded"
        self.name = 'Secret Chamber'
        self.cost = 2

    def special(self, player, game):
        """ Discard any number of cards, +1 gold per card discarded"""
        todiscard = []
        prompt = "Select which card(s) to discard (+1 gold per discard)?"
        while(1):
            options = [{'selector': '0', 'print': 'Discard no more', 'card': None}]
            index = 1
            for c in player.hand:
                s = "%s" % index
                discstr = "Undiscard" if c in todiscard else "Discard"
                options.append({'selector': s, 'print': '%s %s' % (discstr, c.name), 'card': c})
                index += 1
            o = player.userInput(options, prompt)
            if o['card'] is None:
                break
            if o['card'] in todiscard:
                todiscard.remove(o['card'])
            else:
                todiscard.append(o['card'])

        for c in todiscard:
            player.output("Discarding %s" % c.name)
            player.discardCard(c)
        player.t['gold'] += len(todiscard)

    def hook_underAttack(self, player, game):
        """ When another player plans an Attack card, you may reveal
            this from you hand. If you do +2 cards, then put 2 cards
            from your hand on top of your deck """
        if not self.revealCard(player):
            return
        for i in range(2):
            player.pickupCard()
        player.output("Put two cards onto deck")
        for i in range(2):
            self.deckCard(player)

    def deckCard(self, player):
        options = []
        index = 1
        for c in player.hand:
            sel = "%d" % index
            pr = "Put %s to top of deck" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Deck which card?")
        player.addCard(o['card'], 'deck')
        player.hand.remove(o['card'])

    def revealCard(self, player):
        options = [
            {'selector': '0', 'print': "Don't reveal", 'reveal': False},
            {'selector': '1', 'print': 'Reveal', 'reveal': True}
            ]
        o = player.userInput(options, "Reveal Secret Chamber?")
        return o['reveal']

#EOF
