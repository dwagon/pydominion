#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Shield"""
import unittest
from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_Shield(Loot.Loot):
    """Shield"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [
            Card.CardType.REACTION,
            Card.CardType.LOOT,
            Card.CardType.TREASURE,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """$3; +1 Buy; 
        When another player plays an Attack, you may first reveal this from your hand to be unaffected."""
        self.name = "Shield"
        self.coin = 3
        self.buys = 1
        self.cost = 7
        self.pile = "Loot"
        self.defense = True

    def hook_under_attack(self, game, player, attacker):
        player.reveal_card(self)


###############################################################################
class TestShield(unittest.TestCase):
    """Test Shield"""

    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=2, traits=["Cursed"], initcards=["Militia"]
        )
        self.g.start_game()
        self.plr, self.attacker = self.g.player_list()
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Shield":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_playing(self):
        """Test playing"""
        staff = self.g.get_card_from_pile("Loot", "Shield")
        self.plr.add_card(staff, Piles.HAND)
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.play_card(staff)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 3)

    def test_defense(self):
        """Do we defend"""
        staff = self.g.get_card_from_pile("Loot", "Shield")
        self.plr.add_card(staff, Piles.HAND)
        militia = self.g.get_card_from_pile("Militia")
        self.attacker.add_card(militia, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.attacker.play_card(militia)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
