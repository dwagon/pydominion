"""Dominion player using a text interface - generally a human"""

import shutil
import textwrap
from typing import Any, TYPE_CHECKING

from rich.console import Console

from dominion import Piles
from dominion.Card import Card, CardType
from dominion.CardPile import CardPile
from dominion.Option import Option
from dominion.PlayArea import PlayArea
from dominion.Player import Player

if TYPE_CHECKING:
    from dominion.Game import Game

colours = [
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
]


###############################################################################
###############################################################################
###############################################################################
class TextPlayer(Player):
    """Implementation of a text player"""

    def __init__(self, game: "Game", name="", quiet=False, **kwargs: Any) -> None:
        self.colour = colours[kwargs["number"]]
        self.console = Console()
        del kwargs["number"]
        Player.__init__(self, game, name, quiet=quiet, **kwargs)

    ###########################################################################
    def output(self, msg: str, end: str = "\n") -> None:
        self.messages.append(msg)
        if self.quiet:
            return
        prompt = f"[{self.colour}]{self.name}[/]: "
        current_card_stack = ""
        try:
            for card in self.currcards:
                current_card_stack += f"{card.name}> "
        except IndexError:
            pass
        self.console.print(f"{prompt}{current_card_stack}{msg}", end=end)

    ###########################################################################
    def selector_line(self, o: Option) -> str:
        """Print selector line"""
        output: list[str] = []
        output.append(f"{o['selector']})")
        for key in ("print", "verb", "name"):
            if o[key]:
                output.append(o[key])
        if o["details"]:
            output.append(f"({o['details']})")
        if o["name"] and not o["details"] and o["desc"]:
            output.append("-")
        if o["notes"]:
            output.append(o["notes"])

        indent = len(self.name) + 5
        if self.currcards:
            indent += len(self.currcards[0].name) + 2
        desc = ""
        for line in o["desc"].splitlines():
            desc += line.strip() + " "
        output.append(desc)
        text = " ".join(output)
        (cols, _) = shutil.get_terminal_size((80, 24))
        return textwrap.fill(text, subsequent_indent=" " * indent, width=cols - indent)

    ###########################################################################
    def user_input(self, options: list[Option], prompt: str) -> Option:
        """Get input from the user - pick one of the options and return it"""
        for opt in options:
            assert isinstance(opt, Option), f"user_input {opt=} {type(opt)=}"
        for o in options:
            line = self.selector_line(o)
            o["line"] = line
            self.output(line)
        self.output(prompt, end=" ")
        while True:
            if inp := self.get_user_input():
                matching: list[Any] = []
                for o in options:
                    if o["selector"] == inp:
                        return o
                    if inp.lower() in o["line"].lower() and o["selector"] != "-":
                        matching.append(o)
                if len(matching) == 1:
                    return matching[0]
            self.output(f"Invalid Option ({inp})")

    ###########################################################################
    def get_user_input(self) -> str:
        """Get input from user (or the test data)"""
        if self.test_input:
            inp = self.test_input.pop(0)
            self.output(f"Using '{inp}' test input")
        else:  # pragma: no coverage
            try:
                inp = input()
            except (IOError, KeyboardInterrupt):
                self.game.print_state()
                raise
        return inp

    ###########################################################################
    def select_source(self, **kwargs: Any) -> PlayArea:
        """Understand the various places to select cards from - either a
        text description of the source, a list of cards, or by default
        the players hand"""
        if "cardsrc" in kwargs:
            if isinstance(kwargs["cardsrc"], Piles):
                select_from = self.piles[kwargs["cardsrc"]]
            else:
                select_from = kwargs["cardsrc"]
        else:
            select_from = self.piles[Piles.HAND]
        return select_from

    ###########################################################################
    def card_pile_sel(self, num: int = 1, **kwargs: Any) -> list[Any]:
        """Select some card piles from a selection of card piles and return their names"""
        flags: dict[str, Any] = {}
        flags["force"] = kwargs.get("force", False)
        flags["showdesc"] = kwargs.get("showdesc", True)
        flags["verbs"] = kwargs.get("verbs", ("Select", "Unselect"))
        flags["any_num"] = False
        flags["num"] = num

        if "prompt" in kwargs:
            self.output(kwargs["prompt"])

        if kwargs.get("anynum", False):
            flags["any_num"] = True
            flags["num"] = 0

        flags["exclude"] = kwargs.get("exclude", [])
        flags["print_cost"] = kwargs.get("printcost", False)
        flags["print_types"] = kwargs.get("printtypes", False)
        if kwargs.get("cardsrc"):
            piles = [(key, value) for key, value in self.game.get_card_piles() if key in kwargs["cardsrc"]]
        else:
            piles = self.game.get_card_piles()

        selected: list[Any] = []
        while True:
            options = self.card_pile_sel_options(selected, piles, flags)
            ui = self.user_input(options, "Select which card pile?")
            if not ui["card"]:
                break
            if ui["card"] in selected:
                selected.remove(ui["card"])
            else:
                selected.append(ui["card"])
            if num == 1 and len(selected) == 1:
                break
        return selected

    ###########################################################################
    def card_pile_sel_options(
        self, selected: list[Any], piles: list[tuple[str, CardPile]], flags: dict[str, Any]
    ) -> list[Option]:
        """Generate the options for card_pile_sel"""
        options: list[Option] = []
        if self.can_finish(flags["any_num"], flags["force"], flags["num"], len(selected)):
            o = Option(selector="0", verb="Finish Selecting", card=None)
            options.append(o)
        index = 1
        for name, card_pile in piles:
            card = self.game.card_instances[name]
            if card.name in flags["exclude"]:
                continue
            verb = flags["verbs"][0] if card_pile not in selected else flags["verbs"][1]
            o = Option(selector=f"{index}", verb=verb, card=name, name=name)
            index += 1
            if flags["showdesc"]:
                o["desc"] = card.description(self) if card else "Empty card pile"
            if flags["print_cost"]:
                o["details"] = str(self.card_cost(card))
            if flags["print_types"]:
                o["details"] = card.get_cardtype_repr()
            options.append(o)
        return options

    ###########################################################################
    def card_sel(
        self, num: int = 1, **kwargs: Any
    ) -> list["Card"]:  # pylint: disable=too-many-locals, too-many-branches
        """Most interactions with players are the selection of cards
        either from the hand, the drawpiles, or a subset
        * force
            True - Have to select num cards
            False - Can pick less than num cards [Default]
        * cardsrc
            hand - Select the cards from the players hand
            played - Select the cards from the cards played
            discard - Select the cards from the discardpile
        * exclude = [] - Don't let cards in this list be selected
        * printcost
            True - Print out the cost of the cards
            False - Don't print out the cost [Default]
        * printtypes
            True - Print out the types of the cards
            False - Don't print out the types [Default]
        * verbs
            ('Select', 'Unselect')
        * prompt
            What to tell the player at the start
        * anynum
            True - Any number of cards can be selected
        """
        select_from = self.select_source(**kwargs)
        force = kwargs.get("force", False)
        show_desc = kwargs.get("showdesc", True)
        verbs = kwargs.get("verbs", ("Select", "Unselect"))

        if "prompt" in kwargs:
            self.output(kwargs["prompt"])

        if "anynum" in kwargs and kwargs["anynum"]:
            any_num = True
            num = 0
        else:
            any_num = False

        selected: list[Card] = []
        types = kwargs.get("types", {})
        types = self._type_selector(types)
        while True:
            options = []
            if self.can_finish(any_num, force, num, num_selected=len(selected)):
                options.append(Option(selector="0", verb="Finish Selecting", card=None))
            index = 1
            options.extend(self._card_sel_options(index, show_desc, selected, types, select_from, kwargs, verbs))
            ui = self.user_input(options, "Select which card?")
            if not ui["card"]:
                break
            if ui["card"] in selected:
                selected.remove(ui["card"])
            else:
                selected.append(ui["card"])
            if num == 1 and len(selected) == 1:
                break
        return selected

    ###########################################################################
    def can_finish(self, any_num: bool, force: bool, num: int, num_selected: int) -> bool:
        """Can we finish selecting
        any_num - don't care how many
        force - need to be exact
        num - number requested
        num_selected - number that has been selected by the user"""
        if any_num:
            return True
        if force and num == num_selected:
            return True
        if not force and num >= num_selected:
            return True
        return False

    ###########################################################################
    def _card_sel_options(
        self,
        index: int,
        show_desc: bool,
        selected: list[Card],
        types: dict[CardType, bool],
        select_from: PlayArea,
        kwargs: dict[str, Any],
        verbs: tuple[str, str],
    ) -> list[Option]:
        options = []
        for card in sorted(select_from):
            if "exclude" in kwargs and card.name in kwargs["exclude"]:
                continue
            if not self.select_by_type(card, types):
                continue
            if card not in selected:
                verb = verbs[0]
            else:
                verb = verbs[1]
            o = Option(selector=f"{index}", verb=verb, card=card, name=card.name)
            index += 1
            if show_desc:
                o["desc"] = card.description(self)
            if kwargs.get("printcost"):
                o["details"] = str(self.card_cost(card))
            if kwargs.get("printtypes"):
                o["details"] = card.get_cardtype_repr()
            options.append(o)
        return options

    ###########################################################################
    def plr_choose_options(self, prompt: str, *choices: tuple[str, Any]) -> Any:
        index = 0
        options: list[Option] = []
        for prnt, ans in choices:
            options.append(Option(selector=f"{index}", verb=prnt, answer=ans))
            index += 1
        o = self.user_input(options, prompt)
        return o["answer"]


# EOF
