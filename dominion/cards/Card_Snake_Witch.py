#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Snake_Witch"""
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Snake_Witch(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Card; +1 Action; If your hand has no duplicate cards,
            you may reveal it and return this to its pile, to have each other player gain a Curse."""
        self.required_cards = ["Curse"]
        self.name = "Snake Witch"
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """If your hand has no duplicate cards, you may reveal it and return this to its pile, to have each other player gain a Curse."""
        if has_duplicate(player):
            return
        if not player.plr_choose_options(
            "Reveal hand (and return this card) to curse all other players?", ("Keep hidden", False), ("Reveal", True)
        ):
            return
        # Reveal hand
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)

        # Return to its pile
        if self in player.piles[Piles.PLAYED]:
            game.card_piles["Snake Witch"].add(self)
            player.piles[Piles.PLAYED].remove(self)

        # Curse others
        for victim in player.attack_victims():
            player.output(f"{victim} got cursed")
            victim.output(f"{player}'s Snake Witch cursed you")
            try:
                victim.gain_card("Curse")
            except NoCardException:  # pragma: no coverage
                player.output("No more Curses")


###############################################################################
def has_duplicate(player: Player.Player) -> bool:
    hand = set()
    for card in player.piles[Piles.HAND]:
        hand.add(card.name)
    if len(hand) != player.piles[Piles.HAND].size():
        return True
    return False


###############################################################################
class Test_Snake_Witch(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Snake Witch"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.witch = self.g.get_card_from_pile("Snake Witch")

    def test_play_no_duplicates(self) -> None:
        """Play with no duplicates"""
        self.attacker.piles[Piles.DECK].set("Province")
        self.attacker.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.attacker.add_card(self.witch, Piles.HAND)
        self.attacker.test_input = ["Reveal"]
        stack_size = len(self.g.card_piles["Snake Witch"])
        actions = self.attacker.actions.get()
        self.attacker.play_card(self.witch)
        self.assertEqual(self.attacker.actions.get(), actions + 1 - 1)
        self.assertIn("Province", self.attacker.piles[Piles.HAND])
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertNotIn("Snake Witch", self.attacker.piles[Piles.PLAYED])
        self.assertEqual(stack_size + 1, len(self.g.card_piles["Snake Witch"]))

    def test_play_with_duplicates(self) -> None:
        """Play with duplicates"""
        self.attacker.piles[Piles.DECK].set("Province")
        self.attacker.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Gold")
        self.attacker.add_card(self.witch, Piles.HAND)
        actions = self.attacker.actions.get()
        self.attacker.play_card(self.witch)
        self.assertEqual(self.attacker.actions.get(), actions + 1 - 1)
        self.assertIn("Province", self.attacker.piles[Piles.HAND])
        self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Snake Witch", self.attacker.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
