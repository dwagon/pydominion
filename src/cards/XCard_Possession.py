import Game
import Card


##############################################################################
class Card_Possession(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.ALCHEMY
        self.desc = "Be Evil"
        self.name = 'Possession'
        self.cost = 6
        self.required_cards = ['Potion']
        self.potcost = True

    def special(self, game, player):
        """ The player to your left takes an extra turn after this
            one, in which you can see all cards he can and make all
            decisions for him. Any cards he would gain on that turn,
            you gain instead. any cards of his that are trashed are set
            aside and returned to his discard pile at end of turn """
        # TODO

# EOF
