#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Ambassador(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.SEASIDE
        self.desc = """Reveal a card from your hand. Return up to 2 copies of it
        from your hand to the Supply. Then each other player gains a copy of it."""
        self.name = "Ambassador"
        self.cost = 5

    @classmethod
    def pick_card(cls, player):
        while True:
            choice = player.card_sel(
                num=2,
                cardsrc="hand",
                prompt="Return up to 2 copies of this card to the Supply - Other players gain a copy of it",
            )
            if len(choice) == 2:
                if choice[0].name != choice[1].name:
                    player.output("Has to be the same type of card")
                else:
                    return choice
            else:
                return choice

    def special(self, game, player):
        choice = self.pick_card(player)
        if not choice:
            return
        cardname = choice[0].name
        player.reveal_card(choice[0])
        player.output(f"Putting {cardname} back")
        for card in choice:
            player.remove_card(card)
            game[cardname].add(card)
        for plr in player.attack_victims():
            plr.output(f"Gained a {cardname} from {player.name}'s Ambassador")
            plr.gain_card(cardname)


###############################################################################
class Test_Ambassador(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, initcards=["Ambassador"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Ambassador"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.hand.set("Gold", "Duchy", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Duchy", "finish"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.discardpile)
        self.assertNotIn("Duchy", self.plr.hand)

    def test_discard_two(self):
        """Play the card  and discard two"""
        self.plr.hand.set("Duchy", "Duchy", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1", "2", "finish"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.discardpile)
        self.assertNotIn("Duchy", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF