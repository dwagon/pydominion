#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Rogue(Card.Card):
    def __init__(self):
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
    def special(self, game, player):
        if not self.riffle_trash(game, player):
            self.riffle_players(game, player)

    ###########################################################################
    def riffle_players(self, _, player):
        for plr in player.attack_victims():
            self.riffle_victim(plr, player)

    ###########################################################################
    def riffle_victim(self, victim, player):
        cards = []
        for _ in range(2):
            card = victim.next_card()
            victim.reveal_card(card)
            if 3 <= card.cost <= 6:
                cards.append(card)
                card.location = None
            else:
                victim.output(f"{player.name}'s Rogue discarded {card.name} as unsuitable")
                victim.add_card(card, "discard")
        if not cards:
            player.output(f"No suitable cards from {victim.name}")
            return
        options = []
        index = 1
        for card in cards:
            sel = str(index)
            index += 1
            options.append({"selector": sel, "print": f"Trash {card.name}", "card": card})
        o = player.user_input(options, f"Trash which card from {victim.name}?")
        victim.output(f"{player.name}'s rogue trashed your {o['card'].name}'")
        victim.trash_card(o["card"])
        # Discard what the rogue didn't trash
        for card in cards:
            if card != o["card"]:
                victim.output(f"Rogue discarding {card.name} as leftovers")
                victim.discard_card(card)

    ###########################################################################
    def riffle_trash(self, game, player):
        options = []
        picked = set()
        index = 1
        for card in game.trashpile:
            if not card.insupply:
                continue
            if card.name in picked:
                continue
            if 3 <= card.cost <= 6:
                picked.add(card.name)
                sel = f"{index}"
                index += 1
                options.append({"selector": sel, "print": f"Take {card.name}", "card": card})
        if index == 1:
            return False
        o = player.user_input(options, "Pick a card from the trash")
        game.trashpile.remove(o["card"])
        player.add_card(o["card"])
        player.output(f"Took a {o['card'].name} from the trash")
        return True


###############################################################################
class TestRogue(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Rogue", "Moat"],
            badcards=["Pooka", "Fool"],
        )
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Rogue"].remove()

    def test_play(self):
        """Nothing should happen"""
        try:
            self.plr.add_card(self.card, "hand")
            self.plr.play_card(self.card)
            self.assertEqual(self.plr.coins.get(), 2)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_defended(self):
        """Victim has a defense"""
        self.plr.hand.empty()
        self.plr.add_card(self.card, "hand")
        moat = self.g["Moat"].remove()
        self.victim.add_card(moat, "hand")
        self.plr.play_card(self.card)

    def test_good_trash(self):
        """Rogue to get something juicy from the trash"""
        tsize = self.g.trashpile.size()
        for _ in range(2):
            gold = self.g["Gold"].remove()
            self.plr.trash_card(gold)
        self.plr.test_input = ["1"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.g.trashpile.size(), tsize + 1)
            self.assertEqual(self.plr.discardpile.size(), 1)
            self.assertEqual(self.plr.discardpile[-1].name, "Gold")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_good_player(self):
        """Rogue to trash something from another player"""
        tsize = self.g.trashpile.size()
        self.victim.deck.set("Gold", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashpile.size(), tsize + 1)
        self.assertIn("Duchy", self.g.trashpile)
        self.assertEqual(self.victim.discardpile.size(), 1)
        self.assertEqual(self.victim.discardpile[-1].name, "Gold")

    def test_bad_player(self):
        """Rogue to trash nothing from another player"""
        tsize = self.g.trashpile.size()
        self.victim.deck.set("Gold", "Province", "Province")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashpile.size(), tsize)
        self.assertEqual(self.victim.discardpile.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
