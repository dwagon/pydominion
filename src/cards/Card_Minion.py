from Card import Card


class Card_Minion(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'intrigue'
        self.desc = "+1 action, Choose +2 gold or discard"
        self.name = 'Minion'
        self.cost = 5
        self.actions = 1

    def special(self, game, player):
        """ Choose one: +2 gold or
            discard your hand, +4 cards and each other player with
            at least 5 card in hand discards his hand and draws 4
            cards """
        attack = player.plrChooseOptions(
            "What do you want to do?",
            ("+2 gold", False),
            ("Discard your hand, +4 cards and each other player with 5 cards discards and draws 4", True))
        if attack:
            self.attack(game, player)
        else:
            player.addGold(2)

    def attack(self, game, player):
        self.dropAndDraw(player)
        for victim in player.attackVictims():
            if len(victim.hand) >= 5:
                self.dropAndDraw(victim)

    def dropAndDraw(self, plr):
        plr.discardHand()
        plr.pickupCards(4)

#EOF
