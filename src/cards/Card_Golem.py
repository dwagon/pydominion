from Card import Card


class Card_Golem(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Dig through deck for 2 action cards and play them"
        self.name = 'Golem'
        self.cost = 4
        self.potcost = 1

    def special(self, game, player):
        """ Reveal cards from your deck until you reveal 2 Action
            cards other than Golem cards. Discard the other cards, then
            play the Action cards in either order """
        actions = []
        while len(actions) != 2:
            c = player.nextCard()
            if not c:
                player.output("Not enough action cards in deck")
                break
            if c.isAction() and c.name != 'Golem':
                player.pickupCard(card=c)
                actions.append(c)
            else:
                player.output("Drew and discarded %s" % c.name)
        # TODO - let the player choose the order
        for card in actions:
            player.output("Playing %s" % c.name)
            player.playCard(card, costAction=False, discard=False)

#EOF
