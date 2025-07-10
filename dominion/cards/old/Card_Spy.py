#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, NoCardException, Player


###############################################################################
class Card_Spy(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+1 action, +1 cards, reveal next card and optionally discard it"
        self.name = "Spy"
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each player (including you) reveals the top of his deck and either
        discards it or puts it back, your choice"""
        self.spy_on(player, player)
        for pl in player.attack_victims():
            self.spy_on(player, pl)

    def spy_on(self, attacker: Player.Player, victim: Player.Player) -> None:
        try:
            card = victim.next_card()
        except NoCardException:
            return
        victim.reveal_card(card)
        victim_name = "your" if attacker == victim else f"{victim.name}'s"
        if discard := attacker.plr_choose_options(
            f"Discard {victim_name} card?",
            (f"Keep {card} on {victim_name} deck", False),
            (f"Discard {victim_name} {card}", True),
        ):
            victim.add_card(card, Piles.DISCARD)
            victim.output("f{attacker.name}'s Spy discarded your {card}")
        else:
            victim.add_card(card, "topdeck")


###############################################################################
class TestSpy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Spy", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.attacker.piles[Piles.DECK].set("Estate", "Province", "Duchy")
        self.defender.piles[Piles.DECK].set("Estate", "Gold")

    def test_moat(self) -> None:
        self.defender.piles[Piles.HAND].set("Moat")
        spy_card = self.attacker.gain_card("Spy", Piles.HAND)
        assert spy_card is not None
        self.attacker.test_input = ["0"]
        self.attacker.play_card(spy_card)
        self.assertEqual(self.attacker.piles[Piles.DECK][-1].name, "Province")
        self.assertEqual(self.defender.piles[Piles.DECK][-1].name, "Gold")

    def test_undefended(self) -> None:
        scard = self.attacker.gain_card("Spy", Piles.HAND)
        self.attacker.test_input = ["0", "0"]
        self.attacker.play_card(scard)
        self.assertEqual(self.attacker.piles[Piles.DECK][-1].name, "Province")
        self.assertEqual(self.defender.piles[Piles.DECK][-1].name, "Gold")

    def test_discards(self) -> None:
        scard = self.attacker.gain_card("Spy", Piles.HAND)
        self.attacker.test_input = ["1", "1"]
        self.attacker.play_card(scard)
        self.assertEqual(self.attacker.piles[Piles.DECK][-1].name, "Estate")
        self.assertEqual(self.defender.piles[Piles.DECK][-1].name, "Estate")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
