#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Warlord """

import unittest
from collections import Counter
from dominion import Game, Card


###############################################################################
class Card_Warlord(Card.Card):
    """Warlord"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.CLASH,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 5
        self.name = "Warlord"
        self.actions = 1
        self.desc = """+1 Action; At the start of your next turn, +2 Cards.
            Until then, other players can't play an Action from their hand that
            they have 2 or more copies of in play."""

    def hook_all_players_pre_action(
        self, game, player, owner, card
    ):  # pylint: disable=unused-argument
        """Until then, other players can't play an Action from their hand that
        they have 2 or more copies of in play."""
        print(f"DBG hook {player.name=} {owner.name=} {card.name=}")
        if not card.isAction():
            return {}
        cntr = Counter()
        for crd in player.played:
            cntr.update({crd.name: 1})
        print(f"DBG {cntr=}")
        if cntr[card.name] >= 2:
            player.output(
                f"{owner.name}'s Warlord prevents you playing {card.name} more than twice"
            )
            return {"skip_card": True}
        return {}

    def duration(self, game, player):
        """At the start of your next turn, +2 Cards."""
        player.pickup_cards(num=2)


###############################################################################
class Test_Warlord(unittest.TestCase):
    """Test Warlord"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Clashes", "Militia"], use_liaisons=True)
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()

    def test_play(self):
        """Play Card"""
        while True:
            card = self.g["Clashes"].remove()
            if card.name == "Warlord":
                break
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 2)

    def test_others_playing(self):
        """Other players playing actions"""
        while True:
            card = self.g["Clashes"].remove()
            if card.name == "Warlord":
                break
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        mil = self.g["Militia"].remove()
        self.oth.add_card(mil, "hand")
        self.oth.played.set("Militia", "Militia", "Copper")
        self.oth.play_card(mil)
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
