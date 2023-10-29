import sys
import colorama
from typing import Any, TYPE_CHECKING

from dominion import Piles
from dominion.PlayArea import PlayArea
from dominion.Player import Player
from dominion.Option import Option

if TYPE_CHECKING:
    from dominion.Card import Card
    from dominion.Game import Game

if sys.version[0] == "3":
    raw_input = input

colours = [
    colorama.Fore.RED,
    colorama.Fore.GREEN,
    colorama.Fore.YELLOW,
    colorama.Fore.BLUE,
    colorama.Fore.MAGENTA,
    colorama.Fore.CYAN,
]


###############################################################################
###############################################################################
###############################################################################
class TextPlayer(Player):
    def __init__(self, game: "Game", name="", quiet=False, **kwargs: Any) -> None:
        colorama.init()
        self.colour = colours[kwargs["number"]]
        self.quiet = quiet
        del kwargs["number"]
        Player.__init__(self, game, name, **kwargs)

    ###########################################################################
    def output(self, msg: str, end: str = "\n") -> None:
        if not self.quiet:
            sys.stdout.write(f"{self.colour}{self.name}{colorama.Style.RESET_ALL}: ")
            try:
                sys.stdout.write("%s: " % self.currcards[0].name)
            except IndexError:
                pass
            sys.stdout.write(f"{msg}{end}")
        self.messages.append(msg)

    ###########################################################################
    @classmethod
    def wrap(
        cls, text: str, first: int = 0, indent: int = 15, max_width: int = 95
    ) -> str:
        """Wrap the text so that it doesn't take more than maxwidth chars.
        The first line already has "first" characters in it. Subsequent lines
        should be indented "indent" spaces
        """
        out_str: list[str] = []
        sentence: list[str] = []
        if not text:
            return ""
        for word in text.split():
            if len(" ".join(sentence)) + len(word) + first > max_width:
                out_str.append(" ".join(sentence))
                sentence = [" " * indent, word]
                first = 0
            else:
                sentence.append(word.strip())
        out_str.append(" ".join(sentence))
        return "\n".join(out_str)

    ###########################################################################
    def selector_line(self, o: Option | dict[str, Any]) -> str:
        output: list[str] = []
        if isinstance(o, dict):
            verb = o["print"]
            del o["print"]
            newopt = Option(verb=verb, **o)
            o = newopt
        elif isinstance(o, Option):
            pass
        else:
            sys.stderr.write("o is %s\n" % type(o))
        output.append(f"{o['selector']})")
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

        first = len(" ".join(output))
        indent = len(self.name) + 4
        try:
            indent += len(self.currcards[0].name)
        except IndexError:
            pass
        strout = self.wrap(o["desc"], first=first, indent=indent)
        output.append(strout)
        return " ".join(output)

    ###########################################################################
    def user_input(self, options: list[Option | dict[str, Any]], prompt: str) -> Any:
        """Get input from the user"""
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
                try:
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
            if kwargs["cardsrc"] == "hand":
                select_from = self.piles[Piles.HAND]
            elif kwargs["cardsrc"] == "played":
                select_from = self.piles[Piles.PLAYED]
            elif kwargs["cardsrc"] == "discard":
                select_from = self.piles[Piles.DISCARD]
            elif kwargs["cardsrc"] == "exile":
                select_from = self.piles[Piles.EXILE]
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

        if "anynum" in kwargs and kwargs["anynum"]:
            anynum = True
            num = 0
        else:
            anynum = False

        selected: list[Any] = []
        while True:
            options: list[Option] = []
            if (
                anynum
                or (force and num == len(selected))
                or (not force and num >= len(selected))
            ):
                o = Option(selector="0", verb="Finish Selecting", card=None)
                options.append(o)
            index = 1
            for name, card_pile in self.game.get_card_piles():
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
        showdesc = kwargs.get("showdesc", True)
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
            ):
                o = Option(selector="0", verb="Finish Selecting", card=None)
                options.append(o)
            index = 1
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
                if showdesc:
                    o["desc"] = card.description(self)
                if kwargs.get("printcost"):
                    o["details"] = str(self.card_cost(card))
                if kwargs.get("printtypes"):
                    o["details"] = card.get_cardtype_repr()
                options.append(o)
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
    def plr_choose_options(self, prompt: str, *choices: tuple[str, Any]) -> Any:
        index = 0
        options: list[Option] = []
        for prnt, ans in choices:
            options.append(Option(selector=f"{index}", verb=prnt, answer=ans))
            index += 1
        o = self.user_input(options, prompt)
        return o["answer"]


# EOF
