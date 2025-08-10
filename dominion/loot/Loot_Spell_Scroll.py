#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Spell_Scroll"""
import unittest

from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_SpellScroll(Loot.Loot):
    """Spell Scroll"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.LOOT,
            Card.CardType.TREASURE,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Trash this to gain a cheaper card. If it's an Action or Treasure, you may play it."
        self.name = "Spell Scroll"
        self.cost = 7
        self.pile = "Loot"

    def special(self, game, player):
        """Trash this to gain a cheaper card. If it's an Action or Treasure, you may play it."""
        to_trash = player.plr_choose_options("Trash the Spell Scroll?", ("Trash it", True), ("Keep it", False))
        if not to_trash:
            return
        player.trash_card(self)
        gained_card = player.plr_gain_card(cost=6)
        if gained_card.isAction() or gained_card.isTreasure():
            to_play = player.plr_choose_options(f"Play {gained_card}?", ("Play", True), ("Discard", False))
            if to_play:
                player.play_card(gained_card, cost_action=False, discard=False)


###############################################################################
class TestSpellScroll(unittest.TestCase):
    """Test Spell Scroll"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"], badcards=["Gold Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Spell Scroll":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_playing(self):
        """Test playing a spell scroll"""
        spell = self.g.get_card_from_pile("Loot", "Spell Scroll")
        self.plr.add_card(spell, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Trash", "Get Gold", "Play"]
        self.plr.play_card(spell)
        self.assertIn("Spell Scroll", self.g.trash_pile)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
