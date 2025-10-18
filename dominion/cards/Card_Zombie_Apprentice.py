#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Zombie_Apprentice"""
import unittest

from dominion import Game, Card, Piles, Player, PlayArea


###############################################################################
class Card_Zombie_Apprentice(Card.Card):
    """Zombie Apprentice"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ZOMBIE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "You may trash an Action card from your hand for +3 Cards and +1 Action."
        self.name = "Zombie Apprentice"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game: Game.Game) -> None:
        game.trash_pile.add(self)
        self.location = Piles.TRASH

    def special(self, game: Game.Game, player: Player.Player) -> None:
        actions = PlayArea.PlayArea(initial=[_ for _ in player.piles[Piles.HAND] if _.isAction()])
        if not actions:
            player.output("No actions to trash")
            return
        if player.plr_trash_card(prompt="Trash an action from your hand for +3 Cards and +1 Action", cardsrc=actions):
            player.pickup_cards(3)
            player.add_actions(1)


###############################################################################
class TestZombieApprentice(unittest.TestCase):
    """Test Zombie Apprentice"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Zombie Apprentice", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Zombie Apprentice")

    def test_play_no_actions(self) -> None:
        """Play with no actions suitable"""
        tsize = self.g.trash_pile.size()
        self.plr.play_card(self.card, discard=False, cost_action=False)
        self.assertIn("Zombie Apprentice", self.g.trash_pile)
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_play_action(self) -> None:
        """Play with an action"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card, discard=False, cost_action=False)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertIn("Zombie Apprentice", self.g.trash_pile)
        self.assertIn("Moat", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
