#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Jester"""

import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Jester(Card.Card):
    """Jester"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+2 Coin. Each other player discards the top card of their deck.
            If it's a Victory card they gain a Curse; otherwise they gain a copy of the discarded card
            or you do, your choice."""
        self.name = "Jester"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for victim in player.attack_victims():
            jester_attack(player, victim)


###############################################################################
def gain_curse(attacker: Player.Player, victim: Player.Player) -> None:
    """they gain a Curse"""
    try:
        victim.gain_card("Curse")
        victim.output(f"{attacker}'s Jester cursed you")
        attacker.output(f"Cursed {victim}")
    except NoCardException:
        attacker.output("No more Curses")


###############################################################################
def jester_attack(attacker: Player.Player, victim: Player.Player) -> None:
    """Each other player discards the top card of their deck.
    If it's a Victory card they gain a Curse; otherwise they gain a copy of the discarded card,
    or you do, your choice."""
    try:
        card = victim.next_card()
    except NoCardException:
        attacker.output(f"{victim} has no cards!")
        return
    victim.discard_card(card)
    victim.output(f"{attacker}'s Jester discarded your {card}")
    if card.isVictory():
        gain_curse(attacker, victim)
        return
    if not card.insupply:
        attacker.output(f"Card {card} not in supply - no one gets a copy")
        return
    if attacker.plr_choose_options(
        f"Who should get a copy of {victim}'s {card}",
        (f"You get a {card}", True),
        (f"{victim} gets a {card}", False),
    ):
        try:
            attacker.gain_card(card.name)
        except NoCardException:
            attacker.output(f"No more {card.name}")
    else:
        try:
            victim.gain_card(card.name)
            victim.output(f"{attacker}'s Jester gave you a {card}")
        except NoCardException:
            attacker.output(f"No more {card.name}")


###############################################################################
class TestJester(unittest.TestCase):
    """Test Jester"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Jester"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Jester")
        self.plr.add_card(self.card, Piles.HAND)

    def test_victory(self) -> None:
        """Play a jester with the victim having a Victory on top of deck"""
        self.victim.piles[Piles.DECK].set("Duchy")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.victim.piles[Piles.DISCARD])

    def test_give_card(self) -> None:
        """Play a jester and give the duplicate to the victim"""
        self.victim.piles[Piles.DECK].set("Gold")
        self.plr.test_input = ["gets"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        for c in self.victim.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Gold")
        self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.victim.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_take_card(self) -> None:
        """Play a jester and take the duplicate from the victim"""
        self.victim.piles[Piles.DECK].set("Gold")
        self.plr.test_input = ["you"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.victim.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
