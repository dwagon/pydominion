#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Thief"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Thief(Card.Card):
    """Thief"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = """Each other player reveals the top 2 cards of his deck.
            If they revealed any Treasure cards, they trash one of them that you choose.
            You may gain any or all of these trashed cards.
            They discard the other revealed cards."""
        self.name = "Thief"
        self.cost = 4

    def special(self, game, player):  # pylint: disable=unused-argument
        """Each other player reveals the top 2 cards of his deck.
        If they revealed any Treasure cards, they trash one them
        that you choose. You may gain any or all of these trashed
        Cards. They discard the other revealed cards."""

        for pl in player.attack_victims():
            self.thieve_on(pl, player)

    def thieve_on(self, victim, thief):
        """Thieve on a victim"""
        treasures = []
        for _ in range(2):
            c = victim.next_card()
            victim.reveal_card(c)
            if c.isTreasure():
                treasures.append(c)
            else:
                victim.add_card(c, Piles.DISCARD)
        if not treasures:
            thief.output(f"Player {victim.name} has no treasures")
            return
        index = 1
        options = [
            {
                "selector": "0",
                "print": "Don't trash any card",
                "card": None,
                "steal": False,
            }
        ]
        for c in treasures:
            sel = f"{index}"
            pr = f"Trash {c.name} from {victim.name}"
            options.append({"selector": sel, "print": pr, "card": c, "steal": False})
            index += 1
            sel = f"{index}"
            pr = f"Steal {c.name} from {victim.name}"
            options.append({"selector": sel, "print": pr, "card": c, "steal": True})
            index += 1
        o = thief.user_input(options, f"What to do to {victim.name}'s cards?")
        # Discard the ones we don't care about
        for tc in treasures:
            if o["card"] != tc:
                victim.add_card(tc, "discard")
        if o["card"]:
            if o["steal"]:
                thief.add_card(o["card"])
                thief.output(f"Stealing {o['card'].name} from {victim.name}")
                victim.output(f"{thief.name} stole your {o['card'].name}")
            else:
                victim.trash_card(o["card"])
                thief.output(f"Trashed {o['card'].name} from {victim.name}")
                victim.output(f"{thief.name} trashed your {o['card'].name}")


###############################################################################
class TestThief(unittest.TestCase):
    """Test Thief"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Thief", "Moat"])
        self.g.start_game()
        self.thief_card = self.g["Thief"].remove()
        self.thief, self.victim = self.g.player_list()
        self.thief.name = "thief"
        self.victim.name = "victim"
        self.thief.add_card(self.thief_card, Piles.HAND)

    def test_no_treasure(self):
        self.victim.piles[Piles.DECK].set("Estate", "Estate", "Estate")
        self.thief.play_card(self.thief_card)
        self.assertIn("Player victim has no treasures", self.thief.messages)

    def test_moat_defense(self):
        self.victim.piles[Piles.HAND].set("Moat", "Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.thief.play_card(self.thief_card)
        self.assertIn("Player victim is defended", self.thief.messages)
        self.assertEqual(self.victim.piles[Piles.DECK].size(), 3)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 0)

    def test_do_nothing(self):
        self.victim.piles[Piles.HAND].set("Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.thief.test_input = ["Don't trash"]
        self.thief.play_card(self.thief_card)
        self.assertEqual(self.victim.piles[Piles.DECK].size(), 1)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.thief.piles[Piles.DISCARD].size(), 0)

    def test_trash_treasure(self):
        self.victim.piles[Piles.HAND].set("Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.thief.test_input = ["trash gold"]
        self.thief.play_card(self.thief_card)
        # Make sure the gold ends up in the trashpile and not in the victims deck
        self.assertIn("Gold", self.g.trash_pile)
        for card in self.victim.piles[Piles.DECK]:
            self.assertNotEqual(card.name, "Gold")
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Silver")

    def test_steal_treasure(self):
        trash_size = self.g.trash_pile.size()
        self.victim.piles[Piles.HAND].set("Copper", "Copper")
        self.victim.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.thief.test_input = ["steal gold"]
        self.thief.play_card(self.thief_card)
        self.assertEqual(self.g.trash_pile.size(), trash_size)
        for c in self.victim.piles[Piles.DECK]:
            self.assertNotEqual(c.name, "Gold")
        for c in self.thief.piles[Piles.DISCARD]:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail()
        self.assertIn(f"{self.thief.name} stole your Gold", self.victim.messages)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
