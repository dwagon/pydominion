""" http://wiki.dominionstrategy.com/index.php/Way """
from dominion import Card


class Way(Card.Card):
    def special_way(self, game, player, card):
        """Special hook for ways that include the triggering card"""

    def hook_way_discard_this_card(self, game, player, card):
        """Hook called when the card that the way was triggered through is discarded"""


# EOF
