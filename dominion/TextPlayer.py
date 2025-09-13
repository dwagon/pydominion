import shutil
import sys
import textwrap
from typing import Any, TYPE_CHECKING

from rich.console import Console

from dominion import Piles
from dominion.Card import Card, CardType
from dominion.Option import Option
from dominion.PlayArea import PlayArea
from dominion.Player import Player

if TYPE_CHECKING:
    from dominion.Game import Game

if sys.version[0] == "3":
    raw_input = input

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
    def __init__(self, game: "Game", name="", quiet=False, **kwargs: Any) -> None:
        self.colour = colours[kwargs["number"]]
        self.quiet = quiet
        self.console = Console()
        del kwargs["number"]
        Player.__init__(self, game, name, **kwargs)

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
        output: list[str] = []
        output.append(f"{o['selector']})")
        if o["print"]:
            output.append(o["print"])
        if o["verb"]:
            output.append(o["verb"])
        if o["name"]:
            output.append(o["name"])
        if o["details"]:
            output.append(f"({o['details']})")
        if o["name"] and not o["details"] and o["desc"]:
            output.append("-")
        if o["notes"]:
            output.append(o["notes"])

        indent = len(self.name) + 5
        try:
            indent += len(self.currcards[0].name) + 2
        except IndexError:
            pass
        desc = ""
        for line in o["desc"].splitlines():
            desc += line.strip() + " "
        output.append(desc)
        text = " ".join(output)
        (cols, lines) = shutil.get_terminal_size((80, 24))
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
            if self.test_input:
                inp = self.test_input.pop(0)
                self.output(f"Using '{inp}' test input")
            else:
                try:  # pragma: no coverage
                    inp = raw_input()
                except (IOError, KeyboardInterrupt):
                    self.game.print_state()
                    raise
            if inp:
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
        force = kwargs.get("force", False)
        showdesc = kwargs.get("showdesc", True)
        verbs = kwargs.get("verbs", ("Select", "Unselect"))

        if "prompt" in kwargs:
            self.output(kwargs["prompt"])

        if kwargs.get("anynum", False):
            any_num = True
            num = 0
        else:
            any_num = False

        if kwargs.get("cardsrc"):
            piles = [(key, value) for key, value in self.game.get_card_piles() if key in kwargs["cardsrc"]]
        else:
            piles = self.game.get_card_piles()

        selected: list[Any] = []
        while True:
            options: list[Option] = []
            if any_num or (force and num == len(selected)) or (not force and num >= len(selected)):
                o = Option(selector="0", verb="Finish Selecting", card=None)
                options.append(o)
            index = 1
            for name, card_pile in piles:
                card = self.game.card_instances[name]
                if "exclude" in kwargs and card.name in kwargs["exclude"]:
                    continue
                verb = verbs[0] if card_pile not in selected else verbs[1]
                o = Option(selector=f"{index}", verb=verb, card=name, name=name)
                index += 1
                if showdesc:
                    o["desc"] = card.description(self) if card else "Empty card pile"
                if kwargs.get("printcost"):
                    o["details"] = str(self.card_cost(card))
                if kwargs.get("printtypes"):
                    o["details"] = card.get_cardtype_repr()
                options.append(o)
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
            anynum = True
            num = 0
        else:
            anynum = False

        selected: list[Card] = []
        types = kwargs.get("types", {})
        types = self._type_selector(types)
        while True:
            options = []
            if (
                anynum
                or (force and num == len(selected))
                or (not force and num >= len(selected))
                or (len(select_from) < num)
            ):
                o = Option(selector="0", verb="Finish Selecting", card=None)
                options.append(o)
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
