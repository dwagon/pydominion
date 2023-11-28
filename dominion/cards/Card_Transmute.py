#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Transmute(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "Trash a card from hand to gain others"
        self.name = "Transmute"
        self.cost = 0
        self.required_cards = ["Potion"]
        self.potcost = True

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. If it is an...
        Action card, gain a Duchy, Treasure card, gain a Transmute,
        Victory card, gain a gold"""
        player.output("Trash a card to gain...")
        options = [
            {"selector": "0", "print": "Trash Nothing", "card": None, "gain": None}
        ]
        index = 1
        for card in player.piles[Piles.HAND]:
            trash_tag = None
            if card.isAction():
                trash_tag = "Duchy"
            elif card.isTreasure():
                trash_tag = "Transmute"
            elif card.isVictory():
                trash_tag = "Gold"
            if trash_tag is None:
                continue
            pr = f"Trash {card} for {trash_tag}"
            options.append(
                {"selector": f"{index}", "print": pr, "card": card, "gain": trash_tag}
            )
            index += 1
        o = player.user_input(options, "Trash which card?")
        if not o["card"]:
            return
        player.trash_card(o["card"])
        if o["gain"] != "Nothing":
            try:
                player.gain_card(o["gain"])
            except NoCardException:
                player.output(f"No more {o['gain']}")


###############################################################################
class TestTransmute(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Transmute"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Transmute")

    def test_play(self) -> None:
        """Play a transmute - trash nothing"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash nothing"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())

    def test_trash_treasure(self) -> None:
        """Transmute a treasure card to gain a Transmute"""
        self.plr.piles[Piles.HAND].set("Gold", "Estate", "Transmute")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Transmute")

    def test_trash_action(self) -> None:
        """Transmute a action card to gain a Duchy"""
        self.plr.piles[Piles.HAND].set("Gold", "Estate", "Transmute")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash transmute"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Duchy")

    def test_trash_victory(self) -> None:
        """Transmute a victory card to gain a Gold"""
        self.plr.piles[Piles.HAND].set("Gold", "Estate", "Transmute")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash estate"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
