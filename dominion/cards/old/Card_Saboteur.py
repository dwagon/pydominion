#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Saboteur"""

import unittest
from typing import Optional

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Saboteur(Card.Card):
    """Saboteur"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """Each other player reveals cards from the top of his deck
            until revealing one costing 3 Coin or more. He trashes that card
            and may gain a card costing at most 2 Coin less than it. He discards
            the revealed cards."""
        self.name = "Saboteur"
        self.cost = 5

    def special(
        self, game: "Game.Game", player: "Player.Player"
    ) -> None:  # pylint: disable=unused-argument
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

    def pickCard(
        self, victim: "Player.Player", player: "Player.Player"
    ) -> Optional[Card.Card]:
        """Pick Card"""
        for _ in range(len(victim.all_cards())):
            card = victim.next_card()
            if card is None:
                break
            victim.reveal_card(card)
            if card.cost >= 3:
                return card
            victim.output(f"Saboteur checking and discarding {card}")
            victim.discard_card(card)
        victim.output("Don't have any suitable cards")
        player.output(f"{victim} doesn't have any suitable cards")
        return None


###############################################################################
def botresponse(
    player, kind, args=None, kwargs=None
):  # pragma: no coverage, pylint: disable=unused-argument
    """Bot response"""
    to_get = []
    for card in kwargs["cardsrc"]:
        if card.name in ("Copper", "Silver", "Gold"):
            to_get.append((card.cost, card))
    if to_get:
        return [sorted(to_get)[-1][1]]
    return []


###############################################################################
class TestSaboteur(unittest.TestCase):
    """Test Saboteur"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2,
            oldcards=True,
            initcards=["Saboteur"],
            badcards=["Blessed Village", "Cemetery", "Necromancer", "Animal Fair"],
        )
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Saboteur")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a saboteur"""
        trash_size = self.g.trash_pile.size()
        try:
            self.victim.test_input = ["Get Estate"]
            self.victim.piles[Piles.DECK].set("Gold", "Copper", "Estate")
            self.plr.play_card(self.card)
            self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
            trashed = self.g.trash_pile[0]
            self.assertTrue(trashed.cost >= 3)
            for crd in self.victim.piles[Piles.DISCARD]:
                self.assertTrue(crd.cost < 3)
            self.assertTrue(
                self.victim.piles[Piles.DISCARD][-1].cost <= trashed.cost - 2
            )
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_no_matching(self) -> None:
        """Play a saboteur where the victim doesn't have a suitable card"""
        trash_size = self.g.trash_pile.size()
        self.victim.piles[Piles.DECK].set("Copper", "Copper", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), trash_size)
        for card in self.victim.piles[Piles.DISCARD]:
            self.assertTrue(card.cost < 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
