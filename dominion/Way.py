""" http://wiki.dominionstrategy.com/index.php/Way """
from typing import Optional, TYPE_CHECKING, Any
from dominion.Card import Card

if TYPE_CHECKING:
    from dominion.Game import Game
    from dominion.Player import Player


###########################################################################
class Way(Card):
    def special_way(
        self, game: "Game", player: "Player", card: "Card"
    ) -> Optional[dict[str, Any]]:
        """Special hook for ways that include the triggering card"""

    def hook_way_discard_this_card(
        self, game: "Game", player: "Player", card: "Card"
    ) -> None:
        """Hook called when the card that the way was triggered through is discarded"""


# EOF
