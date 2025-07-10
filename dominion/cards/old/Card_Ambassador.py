#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Ambassador"""
import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Ambassador(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Reveal a card from your hand. Return up to 2 copies of it
        from your hand to the Supply. Then each other player gains a copy of it."""
        self.name = "Ambassador"
        self.cost = 5

    @classmethod
    def pick_card(cls, player: Player.Player) -> list[Card.Card] | None:
        if player.piles[Piles.HAND].size() < 2:
            return None
        while True:
            choice = player.card_sel(
                num=2,
                cardsrc=Piles.HAND,
                prompt="Return up to 2 copies of this card to the Supply - Other players gain a copy of it",
            )
            if choice and len(choice) == 2:
                if choice[0].name != choice[1].name:
                    player.output("Has to be the same type of card")
                else:
                    return choice
            else:
                return choice

    def special(self, game: Game.Game, player: Player.Player) -> None:
        choice = self.pick_card(player)
        if not choice:
            return
        card_name = choice[0].name
        player.reveal_card(choice[0])
        player.output(f"Putting {card_name} back")
        for card in choice:
            player.move_card(card, Piles.CARDPILE)
        for victim in player.attack_victims():
            try:
                victim.gain_card(card_name)
                victim.output(f"Gained a {card_name} from {player}'s Ambassador")
            except NoCardException:
                player.output(f"No more {card_name}s")


###############################################################################
class TestAmbassador(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, initcards=["Ambassador"], badcards=["Duchess"], oldcards=True
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Ambassador")

    def test_play(self) -> None:
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Gold", "Duchy", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Duchy", "finish"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.piles[Piles.DISCARD])
        self.assertNotIn("Duchy", self.plr.piles[Piles.HAND])

    def test_discard_two(self) -> None:
        """Play the card and discard two"""
        self.plr.piles[Piles.HAND].set("Duchy", "Duchy", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1", "2", "finish"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.vic.piles[Piles.DISCARD])
        self.assertNotIn("Duchy", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
