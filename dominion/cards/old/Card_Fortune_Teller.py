#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_FortuneTeller(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """2 Coin. Each other player reveals cards from the top of his deck
        until he reveals a Victory or Curse card. He puts it on top and discards the other revealed cards."""
        self.name = "Fortune Teller"
        self.coin = 2
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        for victim in player.attack_victims():
            fortune_attack(victim, player)


###############################################################################
def fortune_attack(victim: "Player.Player", attacker: "Player.Player") -> None:
    max_cards = victim.count_cards()
    while max_cards:
        try:
            card = victim.next_card()
        except NoCardException:
            break
        victim.reveal_card(card)
        if card.isVictory() or card.name == "Curse":
            victim.add_card(card, "topdeck")
            victim.output(f"{attacker}'s Fortune Teller put {card} on top of your deck")
            break
        victim.output(f"{attacker}'s Fortune Teller discarded your {card}")
        victim.discard_card(card)
        max_cards -= 1  # So we don't do it forever


###############################################################################
class Test_FortuneTeller(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Fortune Teller"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Fortune Teller")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Fortune Teller"""
        self.vic.piles[Piles.DECK].set("Duchy", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Silver", self.vic.piles[Piles.DISCARD])
        self.assertIn("Copper", self.vic.piles[Piles.DISCARD])
        self.assertEqual(self.vic.piles[Piles.DECK][-1].name, "Duchy")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
