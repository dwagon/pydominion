#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Golem"""
import unittest

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Golem(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "Dig through deck for 2 action cards and play them"
        self.name = "Golem"
        self.cost = 4
        self.required_cards = ["Potion"]
        self.potcost = True

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Reveal cards from your deck until you reveal 2 Action
        cards other than Golem cards. Discard the other cards, then
        play the Action cards in either order"""
        actions: list[Card.Card] = []
        max_num = len(player.all_cards())
        count = 0
        while len(actions) != 2:
            try:
                card = player.next_card()
            except NoCardException:  # pragma: no coverage
                break
            player.reveal_card(card)
            count += 1
            if card.isAction() and card.name != "Golem":
                actions.append(card)
            else:
                player.output(f"Drew and discarded {card}")
                player.discard_card(card)
            if count > max_num:
                player.output("Not enough action cards in deck")
                break
        # TODO - let the player choose the order
        for card in actions:
            player.output(f"Golem playing {card}")
            player.add_card(card, Piles.HAND)
            player.play_card(card, cost_action=False)


###############################################################################
class TestGolem(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Golem", "Village", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Golem")

    def test_actions(self) -> None:
        """Ensure two actions are picked up and played, others are discarded"""
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Gold", "Gold", "Gold", "Village", "Moat", "Estate", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(
            sorted(["Golem", "Moat", "Village"]),
            sorted([c.name for c in self.plr.piles[Piles.PLAYED]]),
        )
        self.assertEqual(
            sorted(["Copper", "Estate"]),
            sorted([c.name for c in self.plr.piles[Piles.DISCARD]]),
        )

    def test_golem(self) -> None:
        """Ensure golem isn't picked up"""
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.DECK].set("Gold", "Gold", "Gold", "Village", "Golem", "Moat", "Estate", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(
            sorted(["Golem", "Moat", "Village"]),
            sorted([c.name for c in self.plr.piles[Piles.PLAYED]]),
        )
        self.assertEqual(
            sorted(["Copper", "Estate", "Golem"]),
            sorted([c.name for c in self.plr.piles[Piles.DISCARD]]),
        )

    def test_nocards(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Copper", "Copper")
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
