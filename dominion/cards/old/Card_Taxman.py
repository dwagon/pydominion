#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Taxman(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.GUILDS
        self.desc = """You may trash a Treasure from your hand.
        Each other player with 5 or more cards in hand discards a copy of it (or reveals a hand without it).
        Gain a Treasure card costing up to 3 more than the trashed card, putting it on top of your deck."""
        self.name = "Taxman"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        treas = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        cards = player.plr_trash_card(
            cardsrc=treas,
            prompt="Pick card to trash. Others discard that. You gain a treasure costing 3 more",
        )
        if not cards:
            return
        card = cards[0]
        for vic in player.attack_victims():
            if vic.piles[Piles.HAND].size() >= 5:
                if victim_card := vic.piles[Piles.HAND][card.name]:
                    vic.output(f"Discarding {victim_card} due to {player}'s Taxman")
                    player.output(f"{vic} discarded a {victim_card}")
                    vic.discard_card(victim_card)
                else:
                    player.output(f"{vic} doesn't have a {card}")
                    for c in vic.piles[Piles.HAND]:
                        vic.reveal_card(c)
        card_cost = player.card_cost(card) + 3
        player.plr_gain_card(cost=card_cost, types={Card.CardType.TREASURE: True})


###############################################################################
class Test_Taxman(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Taxman"], oldcards=True, badcards=["Fool's Gold"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Taxman")

    def test_play(self) -> None:
        """Play a Taxman"""
        self.plr.piles[Piles.HAND].set("Silver")
        self.victim.piles[Piles.HAND].set("Copper", "Copper", "Estate", "Duchy", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Silver", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.g.trash_pile)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.victim.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
