#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Advisor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = "+1 action, +3 cards, plr to left discards one of them"
        self.name = "Advisor"
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """Reveal the top 3 cards of your deck. The player to your
        left chooses one of them. Discard that card. Put
        the other cards into your hand."""
        cards = []
        choser = game.player_to_left(player)
        for _ in range(3):
            card = player.pickup_card()
            player.reveal_card(card)
            cards.append(card)
        to_discard = choser.card_sel(
            force=True,
            prompt=f"Pick a card of {player.name} to discard from Advisor",
            cardsrc=cards,
            verbs=("Discard", "Undiscard"),
        )[0]
        player.output(f"{choser.name} discarded {to_discard.name}")
        player.discard_card(to_discard)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Discard the card that costs the most
    card_list = [(c.cost, c) for c in kwargs["cardsrc"] if c.isTreasure()]
    if card_list:
        most = sorted(card_list)[-1]
        if most:
            return [most[1]]
    card_list = [(c.cost, c) for c in kwargs["cardsrc"] if c.isAction()]
    if card_list:
        most = sorted(card_list)[-1]
        if most:
            return [most[1]]
    card_list = [(c.cost, c) for c in kwargs["cardsrc"]]
    most = sorted(card_list)[-1]
    return [most[1]]


###############################################################################
class TestAdvisor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Advisor"])
        self.g.start_game()
        self.plr, self.plr2 = self.g.player_list()
        self.acard = self.g.get_card_from_pile("Advisor")
        self.plr.add_card(self.acard, Piles.HAND)

    def test_play(self):
        """ " Play an advisor"""
        self.plr.piles[Piles.DECK].set("Duchy", "Silver", "Gold")
        self.plr2.test_input = ["discard gold"]
        self.plr.play_card(self.acard)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 3 - 1)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
