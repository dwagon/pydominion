#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Zombie_Apprentice(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ZOMBIE]
        self.base = Game.NOCTURNE
        self.desc = (
            "You may trash an Action card from your hand for +3 Cards and +1 Action."
        )
        self.name = "Zombie Apprentice"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game):
        game.trashpile.add(self)

    def special(self, game, player):
        actions = [_ for _ in player.hand if _.isAction()]
        if not actions:
            player.output("No actions to trash")
            return
        tr = player.plrTrashCard(
            prompt="Trash an action from your hand for +3 Cards and +1 Action",
            cardsrc=actions,
        )
        if tr:
            player.pickupCards(3)
            player.addActions(1)


###############################################################################
class Test_Zombie_Apprentice(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Zombie Apprentice", "Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Zombie Apprentice"].remove()

    def test_play_noactions(self):
        tsize = self.g.trashSize()
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertIsNotNone(self.g.in_trash("Zombie Apprentice"))
        self.assertEqual(self.g.trashSize(), tsize)

    def test_play_action(self):
        self.plr.set_hand("Moat")
        self.plr.test_input = ["Moat"]
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertEqual(self.plr.hand.size(), 3)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertIsNotNone(self.g.in_trash("Zombie Apprentice"))
        self.assertIsNotNone(self.g.in_trash("Moat"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
