#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Bandit"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Bandit(Card.Card):
    """Bandit"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = """Gain a Gold. Each other player reveals the top 2 cards
            of their deck, trashes a revealed Treasure other than Copper, and
            discards the rest."""
        self.name = "Bandit"
        self.cost = 5

    def special(self, game, player):
        player.gain_card("Gold")
        for plr in player.attack_victims():
            self._thieve_on(victim=plr, bandit=player)

    @classmethod
    def _thieve_on(cls, victim, bandit):
        """Thieve on the victim"""
        # Each other player reveals the top 2 cards of their deck
        treasures = []
        for _ in range(2):
            card = victim.next_card()
            victim.reveal_card(card)
            if card.isTreasure() and card.name != "Copper":
                treasures.append(card)
            else:
                victim.move_card(card, "discard")
        if not treasures:
            bandit.output(f"Player {victim.name} has no suitable treasures")
            return
        index = 1
        options = [{"selector": "0", "print": "Don't trash any card", "card": None}]
        for card in treasures:
            sel = f"{index}"
            pr = f"Trash {card.name} from {victim.name}"
            options.append({"selector": sel, "print": pr, "card": card})
            sel = f"{index}"
            index += 1
        o = bandit.user_input(options, f"What to do to {victim.name}'s cards?")
        # Discard the ones we don't care about
        for card in treasures:
            if o["card"] == card:
                card.location = None
                victim.trash_card(card)
                bandit.output(f"Trashed {card.name} from {victim.name}")
                victim.output(f"{bandit.name}'s Bandit trashed your {card.name}")
            else:
                victim.add_card(card, "discard")


###############################################################################
class Test_Bandit(unittest.TestCase):
    """Test Bandit"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Bandit"])
        self.g.start_game()
        self.thief, self.vic = self.g.player_list()
        self.thief.name = "MrBandit"
        self.vic.name = "MrVic"
        self.card = self.g["Bandit"].remove()
        self.thief.add_card(self.card, "hand")

    def test_do_nothing(self):
        """Don't trash anything"""
        self.vic.hand.set("Copper", "Copper")
        self.vic.deck.set("Copper", "Silver", "Gold")
        self.thief.test_input = ["Don't trash"]
        self.thief.play_card(self.card)
        self.assertEqual(self.vic.deck.size(), 1)
        self.assertEqual(self.vic.discardpile.size(), 2)

    def test_trash_treasure(self):
        """Trash the treasure"""
        self.vic.hand.set("Copper", "Copper")
        self.vic.deck.set("Copper", "Silver", "Gold")
        self.thief.test_input = ["trash gold"]
        self.thief.play_card(self.card)
        # Make sure the gold ends up in the trashpile and not in the victims deck
        self.assertIn("Gold", self.g.trashpile)
        for card in self.vic.deck:
            self.assertNotEqual(card.name, "Gold")
        self.assertEqual(self.vic.discardpile[0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
