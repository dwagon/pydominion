"""Player is a non-interactive bot of dubious intelligence - big money strategy"""

import inspect
import sys
from typing import Any, TYPE_CHECKING, Optional

import colorama

from dominion import Piles
from dominion.Player import Player

if TYPE_CHECKING:
    from dominion.Game import Game
    from dominion.Card import Card


###############################################################################
###############################################################################
###############################################################################
class BotPlayer(Player):
    """The Bot"""

    def __init__(self, game: "Game", name: str = "", quiet: bool = False, **kwargs: Any):
        colorama.init()
        self.colour = f"{colorama.Back.BLACK}{colorama.Fore.RED}"
        self.quiet = quiet
        Player.__init__(self, game, name, **kwargs)

    ###########################################################################
    def output(self, msg: str, end: str = "\n") -> None:
        self.messages.append(msg)
        if self.quiet:
            return
        current_card_stack = ""

        try:
            for card in self.currcards:
                current_card_stack += f"{card.name}> "
        except IndexError:
            pass
        sys.stdout.write(f"{self.colour}{self.name}{colorama.Style.RESET_ALL}: ")
        sys.stdout.write(f"{current_card_stack}{msg}{end}")

    ###########################################################################
    @classmethod
    def get_options(cls, options):
        try:
            opts = {}
            for opt in options:
                if opt["action"] == "buy":
                    if opt["card"].name == "Colony":
                        opts["colony"] = opt
                    if opt["card"].name == "Province":
                        opts["province"] = opt
                    if opt["card"].name == "Platinum":
                        opts["platinum"] = opt
                    if opt["card"].name == "Gold":
                        opts["gold"] = opt
                    if opt["card"].name == "Duchy":
                        opts["duchy"] = opt
                    if opt["card"].name == "Silver":
                        opts["silver"] = opt
                if opt["action"] == "quit":
                    opts["quit"] = opt
                if opt["action"] == "spendall":
                    opts["spendall"] = opt
            return opts
        except KeyError as exc:  # pragma: no cover
            print(f"Options={options}")
            print(f"Exception: {str(exc)}")
            raise

    ###########################################################################
    def user_input(self, options, prompt: str):  # pylint: disable=too-many-return-statements
        opts = self.get_options(options)
        if "spendall" in opts:
            return opts["spendall"]
        if self.buys.get() == 0:
            return opts["quit"]
        coin = self.coins.get()
        self.output(f"Have {coin} coins")
        if coin >= 11 and "colony" in opts:
            return opts["colony"]
        if coin >= 9 and "platinum" in opts:
            return opts["platinum"]
        if coin >= 8:
            return opts["province"]
        if coin >= 6 and "gold" in opts:
            return opts["gold"]
        if coin >= 5 and "duchy" in opts:
            return opts["duchy"]
        if coin >= 3 and "silver" in opts:
            return opts["silver"]
        return opts["quit"]

    ###########################################################################
    @classmethod
    def get_calling_card(cls) -> Optional[Any]:  # Should be type module
        """Get the module that represents the card doing requiring the response"""
        stack = inspect.stack()
        for rec in stack:
            mod = inspect.getmodule(rec[0])
            assert mod is not None
            mod_name = mod.__name__.replace("dominion.", "")
            if mod_name not in ("BotPlayer", "Player", "__main__"):
                mod = inspect.getmodule(rec[0])
                return mod
        return None

    ###########################################################################
    def check_unexile(self, card_name: str) -> None:
        """Unexile treasure cards if we need to"""
        card = self.game.card_instances[card_name]
        if card.isTreasure():
            self.unexile(card_name)

    ###########################################################################
    def card_sel(self, num: int = 1, **kwargs: Any) -> list["Card"]:
        mod = self.get_calling_card()
        if hasattr(mod, "botresponse"):
            return mod.botresponse(self, "cards", kwargs=kwargs)
        assert False, f"BigMoneyBot can't select cards from {mod.__name__} {kwargs=}"

    ###########################################################################
    def plr_choose_options(self, prompt, *choices):
        mod = self.get_calling_card()
        if hasattr(mod, "botresponse"):
            return mod.botresponse(self, "choices", args=choices)
        assert False, f"BigMoneyBot can't choose options from {mod.__name__} {choices=}"

    ###########################################################################
    def pick_to_discard(self, num_to_discard: int, keepvic: bool = False) -> list["Card"]:
        """Many attacks require this sort of response.
        Return num cards to discard"""
        if num_to_discard <= 0:
            return []
        to_discard = []

        # Discard non-treasures first
        for card in self.piles[Piles.HAND]:
            if card.isTreasure():
                continue
            if keepvic and card.isVictory():
                continue
            to_discard.append(card)
        if len(to_discard) >= num_to_discard:
            return to_discard[:num_to_discard]

        # Discard the cheapest treasures next
        while len(to_discard) < num_to_discard:
            for treas in ("Copper", "Silver", "Gold"):
                for card in self.piles[Piles.HAND]:
                    if card.name == treas:
                        to_discard.append(card)
        if len(to_discard) >= num_to_discard:
            return to_discard[:num_to_discard]
        sys.stderr.write(
            f"Couldn't find cards to discard {num_to_discard} from {', '.join([_.name for _ in self.piles[Piles.HAND]])}"
        )
        sys.stderr.write(f"Managed to get {(', '.join([_.name for _ in to_discard]))} so far\n")
        return []


# EOF
