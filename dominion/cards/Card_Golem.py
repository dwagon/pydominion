#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Golem(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALCHEMY
        self.desc = "Dig through deck for 2 action cards and play them"
        self.name = "Golem"
        self.cost = 4
        self.required_cards = ["Potion"]
        self.potcost = True

    def special(self, game, player):
        """Reveal cards from your deck until you reveal 2 Action
        cards other than Golem cards. Discard the other cards, then
        play the Action cards in either order"""
        actions = []
        maxnum = len(player.allCards())
        count = 0
        while len(actions) != 2:
            c = player.nextCard()
            player.reveal_card(c)
            count += 1
            if count > maxnum:
                player.output("Not enough action cards in deck")
                break
            if c.isAction() and c.name != "Golem":
                player.pickupCard(card=c)
                actions.append(c)
            else:
                player.output("Drew and discarded %s" % c.name)
                player.discardCard(c)
        # TODO - let the player choose the order
        for card in actions:
            player.output("Golem playing %s" % card.name)
            player.playCard(card, costAction=False)


###############################################################################
class Test_Golem(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Golem", "Village", "Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Golem"].remove()

    def test_actions(self):
        """Ensure two actions are picked up and played, others are discarded"""
        self.plr.set_hand()
        self.plr.setDeck("Gold", "Gold", "Gold", "Village", "Moat", "Estate", "Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(
            ["Golem", "Moat", "Village"], [c.name for c in self.plr.played]
        )
        self.assertEqual(["Copper", "Estate"], [c.name for c in self.plr.discardpile])

    def test_golem(self):
        """Ensure golem isn't picked up"""
        self.plr.set_hand()
        self.plr.setDeck(
            "Gold", "Gold", "Gold", "Village", "Golem", "Moat", "Estate", "Copper"
        )
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(
            ["Golem", "Moat", "Village"], [c.name for c in self.plr.played]
        )
        self.assertEqual(
            ["Copper", "Estate", "Golem"], [c.name for c in self.plr.discardpile]
        )

    def test_nocards(self):
        self.plr.set_hand("Copper", "Copper", "Copper")
        self.plr.setDeck("Copper", "Copper", "Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
