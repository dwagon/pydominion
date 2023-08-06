#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Contract """

import unittest
from dominion import Card, Game, PlayArea


###############################################################################
class Card_Contract(Card.Card):
    """Contract"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.TREASURE,
            Card.CardType.DURATION,
            Card.CardType.LIAISON,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Contract"
        self.desc = """$2; +1 Favor; You may set aside an Action from your hand
            to play it at the start of your next turn."""
        self.coin = 2
        self.cost = 5
        self._contract_reserve = PlayArea.PlayArea([])

    def special(self, game, player):
        player.favors.add(1)

    def hook_pre_buy(self, game, player):
        acts = [_ for _ in player.hand if _.isAction()]
        if not acts:
            return
        card = player.card_sel(cardsrc=acts, prompt="Contract: Set aside an action to play next turn")
        self._contract_reserve.add(card[0])
        player.hand.remove(card[0])
        player.secret_count += 1

    def duration(self, game, player):
        for card in self._contract_reserve:
            player.output(f"Removing {card.name} from Contract")
            self._contract_reserve.remove(card)
            player.add_card(card, "hand")
            player.secret_count -= 1
            player.play_card(card)


###############################################################################
class Test_Contract(unittest.TestCase):
    """Test Contract"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Contract", "Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Contract"].remove()

    def test_play_card(self):
        """Play the card"""
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.plr.add_card(self.card, "hand")
        favs = self.plr.favors.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), favs + 1)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.test_input = ["Select Moat", "End Phase"]
        self.plr.buy_phase()
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.played)
        self.assertEqual(self.plr.hand.size(), 5 + 2)  # Hand + Moat


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
