#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Pirate_Ship"""
import unittest

from dominion import Card, Game, Piles, Player, NoCardException

PIRATE_SHIP = "pirate_ship"


###############################################################################
class Card_PirateShip(Card.Card):
    """Pirate Ship"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Choose one: Each other player reveals the top 2 cards of his deck,
            trashes a revealed Treasure that you choose, discards the rest,
            and if anyone trashed a Treasure you take a Coin token;
            or, +1 per Coin token you've taken with Pirate Ships this game."""
        self.name = "Pirate Ship"
        self.cost = 4

    def setup(self, game: "Game.Game") -> None:
        for player in game.player_list():
            player.specials[PIRATE_SHIP] = 0

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        choice = player.plr_choose_options(
            "Pick one",
            (
                """Each other player reveals the top 2 cards of his deck, trashes a
                revealed Treasure that you choose, discards the rest, and if anyone
                trashed a Treasure you take a Coin token""",
                "attack",
            ),
            (
                f"+{player.specials[PIRATE_SHIP]} = +1 per treasure you've taken with Pirate Ships this game.",
                "spend",
            ),
        )
        if choice == "attack":
            trashed = False
            for victim in player.attack_victims():
                if self.attack_player(player, victim):
                    trashed = True
            if trashed:
                player.specials[PIRATE_SHIP] += 1
        else:
            player.coins.add(player.specials[PIRATE_SHIP])

    def attack_player(self, player: "Player.Player", victim: "Player.Player") -> bool:
        trashed = False
        cards = []
        for _ in range(2):
            try:
                card = victim.next_card()
            except NoCardException:
                continue
            victim.reveal_card(card)
            if card.isTreasure():
                cards.append(card)
            else:
                victim.output(f"{player.name}'s Pirate Ship discarded your {card}")
                victim.add_card(card, Piles.DISCARD)
        if cards:
            to_trash = player.plr_trash_card(
                prompt=f"Trash a card from {victim.name}", cardsrc=cards
            )
            if to_trash is None:
                return False
            trashed = True
            for card in cards:
                if card not in to_trash:
                    victim.add_card(card, "discard")
                    victim.output(f"Discarded {card}")
                else:
                    victim.output(f"Trashed {card}")
        else:
            player.output(f"Player {victim.name} has no treasures to trash")
        return trashed


###############################################################################
class TestPirateShip(unittest.TestCase):
    """Test Pirate Ship"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Pirate Ship"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Pirate Ship")
        self.plr.gain_card(new_card=self.card, destination=Piles.HAND)

    def test_play_attack(self) -> None:
        trash_size = self.g.trash_pile.size()
        self.vic.piles[Piles.DECK].set("Copper", "Estate")
        self.plr.test_input = ["Each other", "copper"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
            self.assertIn("Copper", self.g.trash_pile)
            self.assertEqual(self.plr.specials[PIRATE_SHIP], 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_trash_nothing(self) -> None:
        """Play the card but chose to not trash anything"""
        self.vic.piles[Piles.DECK].set("Copper", "Estate")
        self.plr.test_input = ["Each other", "Finish selecting"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.vic.piles[Piles.DISCARD])

    def test_spend(self) -> None:
        self.plr.specials[PIRATE_SHIP] = 2
        self.plr.test_input = ["per treasure"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
