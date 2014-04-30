from Card import Card


class Card_Swindler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 gold. Other players trash top card and gain one with the same cost"
        self.name = 'Swindler'
        self.cost = 3
        self.gold = 2

    def special(self, game, player):
        """ Each other player trashed the top card of his deck and
            gains a card with the same cost that you choose """

        for victim in game.players:
            if victim != player:
                continue
            if victim.hasDefense():
                continue
            card = victim.pickupCard()
            victim.output("Trashing %s" % card.name)
            victim.trashCard(card)
            player.output("Pick which card %s will get" % victim.name)
            victim.plrGainCard(card.cost, modifier='equal', chooser=player, force=True)

#EOF
