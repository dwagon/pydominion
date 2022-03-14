#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bandit(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DOMINION
        self.desc = """Gain a Gold. Each other player reveals the top 2 cards
            of their deck, trashes a revealed Treasure other than Copper, and
            discards the rest."""
        self.name = "Bandit"
        self.cost = 5

    def special(self, game, player):
        player.gain_card("Gold")
        player.output("Gained a Gold")
        for pl in player.attack_victims():
            self.thieveOn(pl, player)

    def thieveOn(self, victim, bandit):
        treasures = []
        for _ in range(2):
            c = victim.next_card()
            victim.reveal_card(c)
            if c.isTreasure() and c.name != "Copper":
                treasures.append(c)
            else:
                victim.add_card(c, "discard")
        if not treasures:
            bandit.output("Player %s has no suitable treasures" % victim.name)
            return
        index = 1
        options = [{"selector": "0", "print": "Don't trash any card", "card": None}]
        for c in treasures:
            sel = "%s" % index
            pr = "Trash %s from %s" % (c.name, victim.name)
            options.append({"selector": sel, "print": pr, "card": c})
            sel = "%s" % index
            index += 1
        o = bandit.userInput(options, "What to do to %s's cards?" % victim.name)
        # Discard the ones we don't care about
        for tc in treasures:
            if o["card"] != tc:
                victim.add_card(tc, "discard")
            else:
                victim.trash_card(o["card"])
                bandit.output("Trashed %s from %s" % (o["card"].name, victim.name))
                victim.output(
                    "%s's Bandit trashed your %s" % (bandit.name, o["card"].name)
                )


###############################################################################
class Test_Bandit(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Bandit"])
        self.g.start_game()
        self.thief, self.vic = self.g.player_list()
        self.thief.name = "MrBandit"
        self.vic.name = "MrVic"
        self.card = self.g["Bandit"].remove()
        self.thief.add_card(self.card, "hand")

    def test_do_nothing(self):
        self.vic.set_hand("Copper", "Copper")
        self.vic.set_deck("Copper", "Silver", "Gold")
        self.thief.test_input = ["Don't trash"]
        self.thief.play_card(self.card)
        self.assertEqual(self.vic.deck.size(), 1)
        self.assertEqual(self.vic.discardpile.size(), 2)

    def test_trash_treasure(self):
        self.vic.set_hand("Copper", "Copper")
        self.vic.set_deck("Copper", "Silver", "Gold")
        self.thief.test_input = ["trash gold"]
        self.thief.play_card(self.card)
        # Make sure the gold ends up in the trashpile and not in the victims deck
        self.assertIsNotNone(self.g.in_trash("Gold"))
        for c in self.vic.deck:
            self.assertNotEqual(c.name, "Gold")
        self.assertEqual(self.vic.discardpile[0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
