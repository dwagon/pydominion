#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Black_Cat """

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Black_Cat(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.REACTION,
        ]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+2 Cards; If it isn't your turn, each other player gains a
            Curse. When another player gains a Victory card, you may play this
            from your hand."""
        self.name = "Black Cat"
        self.cards = 2
        self.cost = 2
        self.required_cards = ["Curse"]

    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        if owner == player:
            return {}
        if card.isVictory():
            for victim in owner.attack_victims():
                try:
                    victim.gain_card("Curse", callhook=False)
                    victim.output(f"{owner}'s Black Cat cursed you")
                    player.output(f"Your Black Cat cursed {victim}")
                except NoCardException:
                    player.output("No more Curse cards")
        return {}


###############################################################################
class TestBlackCat(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Black Cat"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Black Cat")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a card"""
        self.oth.gain_card("Estate")
        self.g.print_state()
        self.assertIn("Curse", self.oth.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
