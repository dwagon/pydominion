#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Fools_Gold(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['treasure', 'reaction']
        self.base = 'hinterland'
        self.desc = """If this is the first time you played a Fool's Gold this turn, this is worth 1 Coin, otherwise it's worth 4 Coin.
        When another player gains a Province, you may trash this from your hand. If you do, gain a Gold, putting it on your deck."""
        self.name = "Fool's Gold"
        self.cost = 2

    def special(self, game, player):
        count = sum([1 for c in player.played if c.name == "Fool's Gold"])
        if count > 1:
            player.output("Gained 4 Coin")
            player.addCoin(4)
        else:
            player.output("Gained 1 Coin")
            player.addCoin(1)

    def hook_allPlayers_gainCard(self, game, player, owner, card):
        if card.name != 'Province':
            return
        if owner == player:
            return
        trash = owner.plrChooseOptions(
            "%s gained a Province. Trash this card to gain a gold?" % player.name,
            ("Keep Fool's Gold", False),
            ("Trash and gain a Gold?", True))
        if trash:
            owner.trashCard(self)
            owner.gainCard('Gold', destination='topdeck')


###############################################################################
class Test_Fools_Gold(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Fool's Gold"])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g["Fool's Gold"].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_once(self):
        """ Play the Fools_Gold """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_play_twice(self):
        """ Play the Fools_Gold again """
        self.plr.setPlayed("Fool's Gold")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 4)

    def test_gain_province(self):
        self.plr.test_input = ['trash']
        self.other.gainCard('Province')
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertEqual(self.g.trashSize(), 1)
        self.assertIsNotNone(self.g.inTrash("Fool's Gold"))

    def test_self_gain_province(self):
        self.plr.gainCard('Province')
        self.assertNotEqual(self.plr.deck[-1].name, 'Gold')
        self.assertEqual(self.g.trashSize(), 0)
        self.assertIsNone(self.g.inTrash("Fool's Gold"))

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF