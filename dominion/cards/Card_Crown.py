#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Crown """

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Crown(Card.Card):
    """Crown"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """If it's your Action phase, you may play an Action from your hand twice.
        If it's your Buy phase, you may play a Treasure from your hand twice."""
        self.name = "Crown"
        self.cost = 5

    def special(self, game, player):
        if player.phase == Player.Phase.ACTION:
            cards = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
            self._do_twice(player, cards)
        if player.phase == Player.Phase.BUY:
            cards = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
            self._do_twice(player, cards)

    def _do_twice(self, player, cards):
        """Do something twice"""
        if not cards:
            player.output("No suitable cards")
            return
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for crd in cards:
            sel = f"{index}"
            pr = f"Play {crd.name} twice"
            options.append({"selector": sel, "print": pr, "card": crd})
            index += 1
        o = player.user_input(options, "Play which card twice?")
        if not o["card"]:
            return
        player.move_after_play(o["card"])
        for i in range(1, 3):
            player.output(f"Number {i} play of {o['card'].name}")
            player.play_card(o["card"], discard=False, cost_action=False)


###############################################################################
class Test_Crown(unittest.TestCase):
    """Test Crown"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Crown", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Crown")

    def test_play(self):
        """Play a crown with no suitable actions"""
        self.plr.piles[Piles.HAND].set("Duchy", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.phase = Player.Phase.ACTION
        self.plr.play_card(self.card)

    def test_action(self):
        """Play a crown with a suitable action"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Copper", "Gold", "Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.phase = Player.Phase.ACTION
        self.plr.test_input = ["moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2 * 2 - 1)

    def test_buy(self):
        """Play a crown in a buy phase"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Copper", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.phase = Player.Phase.BUY
        self.plr.test_input = ["gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
