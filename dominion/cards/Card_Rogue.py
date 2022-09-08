#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Rogue(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DARKAGES
        self.desc = """+2 coin; If there are any cards in the trash costing from 3 to
            6, gain one of them. Otherwise, each other player reveals
            the top 2 cards of his deck, trashes one of the costing
            from 3 to 6, and discards the rest """
        self.name = "Rogue"
        self.coin = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        if not self.riffleTrash(game, player):
            self.rifflePlayers(game, player)

    ###########################################################################
    def rifflePlayers(self, game, player):
        for plr in player.attack_victims():
            self.riffleVictim(plr, player)

    ###########################################################################
    def riffleVictim(self, victim, player):
        cards = []
        for _ in range(2):
            c = victim.next_card()
            victim.reveal_card(c)
            if 3 <= c.cost <= 6:
                cards.append(c)
            else:
                victim.output(f"{player.name}'s Rogue discarded {c.name} as unsuitable")
                victim.add_card(c, "discard")
        if not cards:
            player.output("No suitable cards from %s" % victim.name)
            return
        options = []
        index = 1
        for c in cards:
            sel = "%d" % index
            index += 1
            options.append({"selector": sel, "print": "Trash %s" % c.name, "card": c})
        o = player.user_input(options, "Trash which card from %s?" % victim.name)
        victim.output("%s's rogue trashed your %s" % (player.name, o["card"].name))
        victim.trash_card(o["card"])
        # Discard what the rogue didn't trash
        for c in cards:
            if c != o["card"]:
                victim.output("Rogue discarding %s as leftovers" % c.name)
                victim.discard_card(c)

    ###########################################################################
    def riffleTrash(self, game, player):
        options = []
        picked = set()
        index = 1
        for c in game.trashpile:
            if not c.insupply:
                continue
            if c.name in picked:
                continue
            if 3 <= c.cost <= 6:
                picked.add(c.name)
                sel = "%d" % index
                index += 1
                options.append({"selector": sel, "print": "Take %s" % c.name, "card": c})
        if index == 1:
            return False
        o = player.user_input(options, "Pick a card from the trash")
        game.trashpile.remove(o["card"])
        player.add_card(o["card"])
        player.output("Took a %s from the trash" % o["card"].name)
        return True


###############################################################################
class Test_Rogue(unittest.TestCase):
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
            self.assertEqual(self.plr.get_coins(), 2)
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
