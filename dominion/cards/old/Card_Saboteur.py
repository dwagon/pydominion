#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Saboteur"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Saboteur(Card.Card):
    """ Saboteur """
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.INTRIGUE
        self.desc = """Each other player reveals cards from the top of his deck
            until revealing one costing 3 Coin or more. He trashes that card
            and may gain a card costing at most 2 Coin less than it. He discards
            the revealed cards."""
        self.name = "Saboteur"
        self.cost = 5

    def special(self, game, player):    # pylint: disable=unused-argument
        """Each other player reveals cards from the top of his
        deck until revealing one costing 3 or more. He trashes that
        card and may gain a card costing at most 2 less than it.
        He discards the other revealed cards."""
        for victim in player.attack_victims():
            card = self.pickCard(victim, player)
            if not card:
                continue
            victim.output(f"{player.name}'s saboteur trashed {card.name}")
            victim.trash_card(card)
            victim.plr_gain_card(card.cost - 2)

    def pickCard(self, victim, player):
        """ Pick Card """
        for _ in range(len(victim.all_cards())):
            crd = victim.next_card()
            victim.reveal_card(crd)
            if crd.cost >= 3:
                return crd
            victim.output(f"Saboteur checking and discarding {crd.name}")
            victim.discard_card(crd)
        victim.output("Don't have any suitable cards")
        player.output("%s doesn't have any suitable cards")
        return None


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no coverage, pylint: disable=unused-argument
    """ Bot response """
    toget = []
    for card in kwargs["cardsrc"]:
        if card.name in ("Copper", "Silver", "Gold"):
            toget.append((card.cost, card))
    if toget:
        return [sorted(toget)[-1][1]]
    return []


###############################################################################
class Test_Saboteur(unittest.TestCase):
    """ Test Saboteur """
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            oldcards=True,
            initcards=["Saboteur"],
            badcards=["Blessed Village", "Cemetery", "Necromancer", "Animal Fair"],
        )
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Saboteur"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a saboteur"""
        tsize = self.g.trash_size()
        try:
            self.victim.test_input = ["Get Estate"]
            self.victim.deck.set("Gold", "Copper", "Estate")
            self.plr.play_card(self.card)
            self.assertEqual(self.g.trash_size(), tsize + 1)
            trashed = self.g.trashpile[0]
            self.assertTrue(trashed.cost >= 3)
            for crd in self.victim.discardpile:
                self.assertTrue(crd.cost < 3)
            self.assertTrue(self.victim.discardpile[-1].cost <= trashed.cost - 2)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_nomatching(self):
        """Play a saboteur where the victim doesn't have a suitable card"""
        tsize = self.g.trash_size()
        self.victim.deck.set("Copper", "Copper", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_size(), tsize)
        for crd in self.victim.discardpile:
            self.assertTrue(crd.cost < 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
