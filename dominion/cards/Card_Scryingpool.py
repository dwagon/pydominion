#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Scryingpool(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.ALCHEMY
        self.desc = """+1 Action. Each player (including you) reveals the top card of
        his deck and either discards it or puts it back, your choice.
        Then reveal cards from the top of your deck until you reveal one that is not an Action.
        Put all of your revealed cards into your hand."""
        self.name = "Scrying Pool"
        self.actions = 1
        self.cost = 2
        self.required_cards = ["Potion"]
        self.potcost = True

    def special(self, game, player):
        for plr in player.attack_victims():
            self.discardOrPutBack(plr, player)
        self.discardOrPutBack(player, player)
        revealed = []
        while True:
            topcard = player.pickup_card()
            player.reveal_card(topcard)
            if not topcard.isAction():
                break
            revealed.append(topcard)
        for card in revealed:
            player.add_card(card, "hand")

    def discardOrPutBack(self, victim, player):
        if player == victim:
            name = ("you", "your")
        else:
            name = (victim.name, "%s's" % victim.name)
        topcard = victim.next_card()
        victim.reveal_card(topcard)
        putback = player.plr_choose_options(
            "For %s which one?" % name[0],
            ("Discard %s" % topcard.name, False),
            ("Putback %s" % topcard.name, True),
        )
        if putback:
            victim.output("Put %s back on %s deck" % (topcard.name, name[1]))
            victim.add_card(topcard, "deck")
        else:
            victim.output("Discarded %s" % topcard.name)
            victim.add_card(topcard, "discard")


###############################################################################
class Test_ScryingPool(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Scrying Pool", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Scrying Pool"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a scrying pool"""
        self.plr.deck.set("Moat", "Gold")
        self.vic.deck.set("Duchy")
        self.plr.test_input = ["discard", "putback"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Duchy", self.vic.discardpile)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Moat", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
# EOF
