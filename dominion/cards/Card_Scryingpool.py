#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_ScryingPool(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = """+1 Action. Each player (including you) reveals the top card of
        his deck and either discards it or puts it back, your choice.
        Then reveal cards from the top of your deck until you reveal one that is not an Action.
        Put all of your revealed cards into your hand."""
        self.name = "Scrying Pool"
        self.actions = 1
        self.cost = 2
        self.required_cards = ["Potion"]
        self.potcost = True

    def special(self, game, player):
        for plr in player.attack_victims():
            discard_or_put_back(plr, player)
        discard_or_put_back(player, player)
        revealed = []
        while True:
            top_card = player.pickup_card()
            player.reveal_card(top_card)
            revealed.append(top_card)
            if not top_card.isAction():
                break
        for card in revealed:
            player.add_card(card, Piles.HAND)


###############################################################################
def discard_or_put_back(victim, player):
    if player == victim:
        name = ("you", "your")
    else:
        name = (victim.name, f"{victim.name}'s")
    top_card = victim.next_card()
    if top_card is None:
        return
    victim.reveal_card(top_card)
    putback = player.plr_choose_options(
        f"For {name[0]} which one?",
        (f"Discard {top_card.name}", False),
        (f"Putback {top_card.name}", True),
    )
    if putback:
        victim.output(f"Put {top_card.name} back on {name[1]} deck")
        victim.add_card(top_card, "topdeck")
    else:
        victim.output(f"Discarded {top_card.name}")
        victim.add_card(top_card, "discard")


###############################################################################
class TestScryingPool(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Scrying Pool", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Scrying Pool"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play a scrying pool"""
        self.plr.piles[Piles.DECK].set("Silver", "Province", "Moat", "Gold")
        self.vic.piles[Piles.DECK].set("Duchy")
        self.plr.test_input = ["discard", "discard", "putback"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Duchy", self.vic.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
# EOF
