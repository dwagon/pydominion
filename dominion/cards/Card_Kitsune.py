#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Kitsune"""
import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Kitsune(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK, Card.CardType.OMEN]
        self.base = Card.CardExpansion.RISING_SUN
        self.required_cards = ["Curse"]
        self.desc = (
            """+1 Sun; Choose two different options: +2 Actions; +$2; each other player gains a Curse; gain a Silver."""
        )
        self.name = "Kitsune"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Choose two different options: +2 Actions; +$2; each other player gains a Curse; gain a Silver."""
        unchosen = [
            ("+2 Actions", "actions"),
            ("+$2 Coins", "coin"),
            ("Each other player gains a Curse", "curse"),
            ("Gain a Silver", "silver"),
        ]
        for _ in range(2):
            choice = self._select_option(player, unchosen)
            for opt in unchosen[:]:
                if opt[1] == choice:
                    unchosen.remove(opt)

    def _select_option(self, player: Player.Player, unchosen: list[tuple[str, str]]) -> str:
        choice = player.plr_choose_options("Pick One", *unchosen)
        match choice:
            case "actions":
                player.actions.add(2)
            case "coin":
                player.coins.add(2)
            case "curse":
                for victim in player.attack_victims():
                    player.output(f"{victim} got cursed")
                    victim.output(f"{player}'s Kitsune cursed you")
                    try:
                        victim.gain_card("Curse")
                    except NoCardException:  # pragma: no coverage
                        player.output("No more Curses")
            case "silver":
                try:
                    player.gain_card("Silver")
                except NoCardException:  # pragma: no coverage
                    player.output("No more Silver")
        return choice


###############################################################################
class Test_Kitsune(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Kitsune"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Kitsune")

    def test_play_actions_curse(self) -> None:
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["actions", "curse"]
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), actions + 2 - 1)

    def test_play_coin_silver(self) -> None:
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["coin", "silver"]
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.coins.get(), coins + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
