#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Rogue"""
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Rogue(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 coin; If there are any cards in the trash costing from 3 to
            6, gain one of them. Otherwise, each other player reveals
            the top 2 cards of his deck, trashes one of the costing
            from 3 to 6, and discards the rest """
        self.name = "Rogue"
        self.coin = 2
        self.cost = 5

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        if not self.riffle_trash(game, player):
            self.riffle_players(game, player)

    ###########################################################################
    def riffle_players(self, _: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            self.riffle_victim(plr, player)

    ###########################################################################
    def riffle_victim(self, victim: Player.Player, player: Player.Player) -> None:
        cards = []
        for _ in range(2):
            try:
                card = victim.next_card()
            except NoCardException:
                continue
            victim.reveal_card(card)
            if 3 <= card.cost <= 6:
                cards.append(card)
                card.location = None
            else:
                victim.output(
                    f"{player.name}'s Rogue discarded {card.name} as unsuitable"
                )
                victim.add_card(card, "discard")
        if not cards:
            player.output(f"No suitable cards from {victim.name}")
            return
        options = []
        index = 1
        for card in cards:
            sel = str(index)
            index += 1
            options.append(
                {"selector": sel, "print": f"Trash {card.name}", "card": card}
            )
        o = player.user_input(options, f"Trash which card from {victim.name}?")
        victim.output(f"{player.name}'s rogue trashed your {o['card']}'")
        victim.trash_card(o["card"])
        # Discard what the rogue didn't trash
        for card in cards:
            if card != o["card"]:
                victim.output(f"Rogue discarding {card} as leftovers")
                victim.discard_card(card)

    ###########################################################################
    def riffle_trash(self, game: Game.Game, player: Player.Player) -> bool:
        options = []
        picked = set()
        index = 0
        for card in game.trash_pile:
            if not card.insupply:
                continue
            if card.name in picked:
                continue
            if 3 <= card.cost <= 6:
                picked.add(card.name)
                index += 1
                options.append(
                    {"selector": f"{index}", "print": f"Take {card}", "card": card}
                )
        if index == 0:
            return False
        o = player.user_input(options, "Pick a card from the trash")
        game.trash_pile.remove(o["card"])
        player.add_card(o["card"])
        player.output(f"Took a {o['card']} from the trash")
        return True


###############################################################################
class TestRogue(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Rogue", "Moat"],
            badcards=["Pooka", "Fool"],
        )
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Rogue")

    def test_play(self) -> None:
        """Nothing should happen"""
        try:
            self.plr.add_card(self.card, Piles.HAND)
            self.plr.play_card(self.card)
            self.assertEqual(self.plr.coins.get(), 2)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_defended(self) -> None:
        """Victim has a defense"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        moat = self.g.get_card_from_pile("Moat")
        self.victim.add_card(moat, Piles.HAND)
        self.plr.play_card(self.card)

    def test_good_trash(self) -> None:
        """Rogue to get something juicy from the trash"""
        trash_size = self.g.trash_pile.size()
        for _ in range(2):
            gold = self.g.get_card_from_pile("Gold")
            self.plr.trash_card(gold)
        self.plr.test_input = ["1"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
            self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_good_player(self) -> None:
        """Rogue to trash something from another player"""
        trash_size = self.g.trash_pile.size()
        self.victim.piles[Piles.DECK].set("Gold", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Gold", self.victim.piles[Piles.DISCARD])

    def test_bad_player(self) -> None:
        """Rogue to trash nothing from another player"""
        trash_size = self.g.trash_pile.size()
        self.victim.piles[Piles.DECK].set("Gold", "Province", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), trash_size)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
