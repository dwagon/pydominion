#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Swamp_Hag"""

import unittest

from dominion import Game, Card, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_SwampHag(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """Until your next turn, when any other player buys a card, he gains a Curse.
        At the start of your next turn: +3 Coin"""
        self.required_cards = ["Curse"]
        self.name = "Swamp Hag"
        self.cost = 5

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        player.coins.add(3)
        return {}

    def hook_all_players_buy_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> None:
        if player == owner:
            return
        try:
            player.gain_card("Curse")
            player.output(f"Gained a curse from {owner}'s Swamp Hag")
            owner.output(f"Cursed {player} when they bought a {card}")
        except NoCardException:
            owner.output("No more Curses")


###############################################################################
class TestSwampHag(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Swamp Hag"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.seahag = self.g.get_card_from_pile("Swamp Hag")
        self.attacker.add_card(self.seahag, Piles.HAND)

    def test_play(self) -> None:
        self.attacker.play_card(self.seahag)
        self.attacker.end_turn()
        self.victim.buy_card("Copper")
        self.assertEqual(self.attacker.piles[Piles.DURATION][0].name, "Swamp Hag")
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.attacker.start_turn()
        self.assertIn("Swamp Hag", self.attacker.piles[Piles.PLAYED])
        self.assertEqual(self.attacker.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
