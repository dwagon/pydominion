from Card import Card


class Card_Steward(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Chose: +2 cards, +2 gold, trash 2 cards"
        self.name = 'Steward'
        self.cost = 3

    def special(self, game, player):
        """ Choose one: +2 Cards; or +2 gold, or trash 2 cards from your hand """
        options = [
            {'selector': '0', 'print': '+2 Cards', 'choose': 'cards'},
            {'selector': '1', 'print': '+2 Gold', 'choose': 'gold'},
            {'selector': '2', 'print': 'Trash 2', 'choose': 'trash'}
            ]
        o = player.userInput(options, "Choose one?")
        if o['choose'] == 'cards':
            for i in range(2):
                player.pickupCard()
            return
        if o['choose'] == 'gold':
            player.t['gold'] += 2
            return
        if o['choose'] == 'trash':
            player.output("Trash two cards")
            for i in range(2):
                player.plrTrashCard()
            return

#EOF
