#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Raider"""
import unittest
from dominion import Game, Card, Piles, Phase, Player, OptionKeys


###############################################################################
class Card_Raider(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.NIGHT,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Each other player with 5 or more cards in hand discards
            a copy of a card you have in play (or reveals they can't). At the
            start of your next turn, +3 Coins"""
        self.name = "Raider"
        self.cost = 6

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        player.coins.add(3)
        return {}

    def night(self, game: Game.Game, player: Player.Player) -> None:
        in_play = {_.name for _ in player.piles[Piles.PLAYED]}
        for victim in player.attack_victims():
            if victim.piles[Piles.HAND].size() >= 5:
                player.output(f"Raiding {victim}")
                to_discard = []
                for card in victim.piles[Piles.HAND]:
                    if card.name in in_play:
                        victim.output(f"{player.name}'s Raider discarded your {card}")
                        player.output(f"Raider discarded {victim}'s {card}")
                        to_discard.append(card)
                if not to_discard:
                    for card in victim.piles[Piles.HAND]:
                        victim.reveal_card(card)
                for card in to_discard[:]:
                    victim.discard_card(card)


###############################################################################
class TestRaider(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Raider"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Raider")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Raider"""
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.PLAYED].set("Gold", "Silver")
        self.victim.piles[Piles.HAND].set(
            "Silver", "Gold", "Estate", "Copper", "Copper"
        )
        self.plr.play_card(self.card)
        try:
            self.assertIn("Gold", self.victim.piles[Piles.DISCARD])
            self.assertIn("Silver", self.victim.piles[Piles.DISCARD])
            self.assertNotIn("Gold", self.victim.piles[Piles.HAND])
            self.assertNotIn("Silver", self.victim.piles[Piles.HAND])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise
        self.plr.end_turn()
        self.plr.start_turn()
        try:
            self.assertEqual(self.plr.coins.get(), 3)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
