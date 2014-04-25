from Card import Card


class Card_Bishop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a card for VP"
        self.name = 'Bishop'
        self.gold = 1
        self.victory = 1
        self.cost = 4

    def special(self, game, player):
        """ Trash a card from your hand. +VP equal to half its cost
        in coins, rounded down. Each other player may trash a card
        from his hand """
        player.output("Trash a card.")
        options = [{'selector': '0', 'print': "Don't trash a card", 'card': None}]
        index = 1
        for c in player.hand:
            sel = "%d" % index
            pr = "Trash %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Trash which card?")
        if not o['card']:
            return
        points = int(o['card'].cost / 2)
        player.basescore += points
        player.output("Trashing %s for %d points" % (o['card'].name, points))
        player.trashCard(o['card'])

#EOF
