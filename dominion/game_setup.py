"""Functions used to set up the game"""

import glob
import importlib
import os
import random
import sys
import uuid
from enum import StrEnum, auto
from typing import TYPE_CHECKING, cast, Optional

from dominion import Keys
from dominion import Piles
from dominion.Boon import BoonPile
from dominion.BotPlayer import BotPlayer
from dominion.Card import CardExpansion, Card
from dominion.CardPile import CardPile
from dominion.Event import Event
from dominion.Hex import HexPile
from dominion.Landmark import Landmark
from dominion.Loot import LootPile
from dominion.Names import playerNames
from dominion.Player import Player
from dominion.RandobotPlayer import RandobotPlayer
from dominion.TextPlayer import TextPlayer
from dominion.Way import Way

if TYPE_CHECKING:  # pragma: no coverage
    from dominion.Game import Game


class Flags(StrEnum):
    ALLOW_SHELTERS = auto()
    LOADED_TRAVELLERS = auto()
    LOADED_PRIZES = auto()
    ALLOW_POTIONS = auto()


###########################################################################
def use_shelters_in_game(game: "Game", allow_shelters: bool, specified: list[str]) -> bool:
    """Should we use shelters"""
    if "shelters" in [_.lower() for _ in specified]:
        return True
    if not allow_shelters:
        return False

    # Pick a card to see if it is a dark ages card
    halfway = len(game.card_piles) // 2
    name, card_pile = list(game.card_piles.items())[halfway]
    card = game.card_instances[name]
    if card.base == CardExpansion.DARKAGES:
        return True

    return False


###########################################################################
def setup_shelters(game: "Game") -> None:
    game.card_piles["Shelters"] = CardPile(game)
    for _ in range(game.numplayers):
        shelters = ["Overgrown Estate", "Hovel", "Necropolis"]
        for shelter in shelters:
            game.card_instances[shelter] = game.card_mapping["Shelter"][shelter]()
            shelter_card = game.card_mapping["Shelter"][shelter]()
            game.card_piles["Shelters"].add(shelter_card)


###########################################################################
def load_travellers(game: "Game") -> None:
    """TODO"""
    travellers = game.getAvailableCards("Traveller")
    for trav in travellers:
        use_card_pile(game, None, trav, True, "Traveller")


############################################################################
def load_loot(game: "Game") -> None:
    """Load Loot cards into game"""
    if "Loot" in game.card_piles:
        return
    game.output("Using Loot cards")
    game.card_piles["Loot"] = LootPile(game)
    game.card_piles["Loot"].init_cards()


###########################################################################
def load_ways(game: "Game", specified: list[str], num_required: int) -> dict[str, Way]:
    """Load required Ways"""
    way_cards = []
    for way_name in specified:
        if not way_name.lower().startswith("way of the "):
            way_cards.append(f"Way of the {way_name}")
        else:
            way_cards.append(way_name)
    ways = load_non_kingdom_cards(
        game,
        cardtype="Way",
        specified=way_cards,
        num_required=num_required,
    )
    if ways:
        game.output(f"Playing with {ways}")
    return ways


###########################################################################
def load_events(game: "Game", specified: list[str], num_required: int) -> dict[str, Event]:
    """Load required events"""
    events = load_non_kingdom_cards(
        game,
        cardtype="Event",
        specified=specified,
        num_required=num_required,
    )
    if events:
        game.output(f"Playing with Events: {', '.join(events)}")
    return cast(dict[str, Event], events)


###########################################################################
def load_hexes(game: "Game") -> None:
    """Load Hexes into Pile"""
    if game.hexes:
        return
    game.output("Using hexes")
    d = load_non_kingdom_pile(game, "Hex", HexPile)
    game.hexes = list(d.values())
    random.shuffle(game.hexes)


###########################################################################
def load_projects(game: "Game", specified: list[str], num_required: int) -> None:
    """TODO"""
    if game.projects:
        return
    game.projects = load_non_kingdom_cards(
        game,
        "Project",
        specified,
        num_required,
    )
    if game.projects:
        game.output(f"Playing with Project {game.projects}")


###########################################################################
def load_artifacts(game: "Game") -> None:
    """TODO"""
    if game.artifacts:
        return
    game.artifacts = load_non_kingdom_cards(game, "Artifact", [], None)
    game.output("Playing with Artifacts")


###########################################################################
def load_landmarks(game: "Game", specified: list[str], num_required: int) -> dict[str, Landmark]:
    """Load required landmarks"""
    landmarks = load_non_kingdom_cards(
        game,
        "Landmark",
        specified,
        num_required,
    )
    if landmarks:
        game.output(f"Playing with Landmarks {landmarks}")
    return landmarks


###########################################################################
def load_traits(game: "Game", specified: list[str], num_required: int) -> None:
    """Load required Traits"""
    game.traits = load_non_kingdom_cards(
        game,
        cardtype="Trait",
        specified=specified,
        num_required=num_required,
    )
    for trait in game.traits:
        card_piles = []
        for pile in game.card_piles:
            if game.card_piles[pile].trait:
                continue
            if pile in game._base_cards:
                continue
            if pile in ("Loot",):
                continue
            card = game.card_instances[pile]
            if not card.purchasable:
                continue
            if not card.isAction() and not card.isTreasure():
                continue
            card_piles.append(pile)
        card_pile = random.choice(card_piles)
        game.assign_trait(trait, card_pile)


###########################################################################
def load_states(game: "Game") -> None:
    """Load States"""
    if game.states:
        return
    game.output("Using states")
    game.states = load_non_kingdom_cards(game, "State", [], None)


###########################################################################
def load_boons(game: "Game") -> None:
    """Load boons into Pile"""
    if game.boons:
        return
    game.output("Using boons")
    d = load_non_kingdom_pile(game, "Boon", BoonPile)
    game.boons = list(d.values())
    random.shuffle(game.boons)


###########################################################################
def load_ally(game: "Game", specified: list[str]) -> Card:
    """Load the ally"""
    if isinstance(specified, str):
        specified = [specified]
    allies = load_non_kingdom_cards(game, "Ally", specified, 1)
    ally = list(allies.values())[0]
    game.output(f"Playing with Ally {ally}")
    return ally


###########################################################################
def get_card_classes(prefix: str, path: str, class_prefix: str = "Card_") -> dict[str, type[Card]]:
    """Import all the modules to determine the real name of the card
    This is slow, but it is the only way that I can think of

    Look in {path} for files starting with {prefix}
    """
    mapping: dict[str, type[Card]] = {}
    files = glob.glob(f"{path}/{prefix}_*.py")
    for file_name in [os.path.basename(_) for _ in files]:
        file_name = file_name.replace(".py", "")
        mod = importlib.import_module(f"{path.replace('/', '.')}.{file_name}")

        # Find the class in the module that is the one we want (e.g. Card_Foo)
        classes = dir(mod)
        for kls in classes:
            if kls.startswith(class_prefix):
                klass = getattr(mod, kls)
                break
        else:  # pragma: no cover
            raise ImportError(f"Couldn't find {prefix} class in {path}\n")
        mapping[klass().name] = klass
        klass().check()
    return mapping


###########################################################################
def add_prizes(game: "Game") -> None:
    """TODO"""
    for prize in game.getAvailableCards("PrizeCard"):
        use_card_pile(game, None, prize, False, "PrizeCard")


###########################################################################
def use_ruins(game: "Game") -> None:
    """Use Ruins"""
    use_card_pile(game, None, "Ruins", True)


###########################################################################
def check_card_requirement(game: "Game", card: Card) -> None:
    for x in card.required_cards:
        if x == "Loot":
            load_loot(game)
            continue
        if isinstance(x, tuple):
            card_type, card_name = x
        else:
            card_type, card_name = "BaseCard", x
        if card_name not in game.card_piles:
            use_card_pile(game, None, card_name, force=True, card_type=card_type)
            game.output(f"Playing with {card_name} as required by {card}")

    if card.heirloom is not None and card.heirloom not in game.heirlooms:
        use_card_pile(game, None, card.heirloom, force=True, card_type="Heirloom")
        game.heirlooms.append(card.heirloom)
        game.output(f"Playing with {card.heirloom} as required by {card}")

    if card.isLooter() and "Ruins" not in game.card_piles:
        use_ruins(game)
        game.output(f"Playing with Ruins as required by {card}")
    if card.isFate() and not game.boons:
        load_boons(game)
    if card.isDoom() and not game.hexes:
        load_hexes(game)
        game.output(f"Using hexes as required by {card}")
    if card.isLiaison() and not game.ally:
        game.ally = load_ally(game, game.init[Keys.ALLIES])
        game.output(f"Using Allies as required by {card}")
    if card.traveller and not game.flags[Flags.LOADED_TRAVELLERS]:
        load_travellers(game)
        game.flags[Flags.LOADED_TRAVELLERS] = True
    if card.needs_prizes and not game.flags[Flags.LOADED_PRIZES]:
        add_prizes(game)
        game.flags[Flags.LOADED_PRIZES] = True
        game.output(f"Playing with Prizes as required by {card}")
    if card.needsartifacts and not game.artifacts:
        load_artifacts(game)
        game.output(f"Using artifacts as required by {card}")
    if card.needsprojects and not game.projects:
        load_projects(game, game.init[Keys.PROJECTS], game.init_numbers[Keys.PROJECTS])
        game.output(f"Using projects as required by {card}")


###########################################################################
def get_available_card_classes(game: "Game") -> dict[str, dict[str, type[Card]]]:
    """Create a mapping between the card name and the module of that card"""
    mapping: dict[str, dict[str, type[Card]]] = {}
    for prefix in (
        "Card",
        "BaseCard",
        "Traveller",
        "PrizeCard",
        "Castle",
        "Heirloom",
        "Shelter",
        "Split",
    ):
        mapping[prefix] = get_card_classes(prefix, game.paths[Keys.CARDS], "Card_")
        if game.oldcards:
            old_path = os.path.join(game.paths[Keys.CARDS], "old")
            mapping[prefix].update(get_card_classes(prefix, old_path, "Card_"))
    mapping["Event"] = get_card_classes("Event", game.paths[Keys.EVENT], "Event_")
    mapping["Way"] = get_card_classes("Way", game.paths[Keys.WAY], "Way_")
    mapping["Landmark"] = get_card_classes("Landmark", game.paths[Keys.LANDMARK], "Landmark_")
    mapping["Boon"] = get_card_classes("Boon", game.paths[Keys.BOONS], "Boon_")
    mapping["Hex"] = get_card_classes("Hex", game.paths[Keys.HEXES], "Hex_")
    mapping["State"] = get_card_classes("State", game.paths[Keys.STATES], "State_")
    mapping["Artifact"] = get_card_classes("Artifact", game.paths[Keys.ARTIFACTS], "Artifact_")
    mapping["Project"] = get_card_classes("Project", game.paths[Keys.PROJECTS], "Project_")
    mapping["Ally"] = get_card_classes("Ally", game.paths[Keys.ALLIES], "Ally_")
    mapping["Trait"] = get_card_classes("Trait", game.paths[Keys.TRAITS], "Trait_")
    mapping["Loot"] = get_card_classes("Loot", game.paths[Keys.LOOT], "Loot_")
    return mapping


###########################################################################
def load_non_kingdom_pile(game: "Game", cardtype: str, pileClass) -> dict[str, CardPile]:
    """Load non kingdom cards into a pile
    Returns a dictionary; key is the name, value is the instance
    """
    dest: dict[str, CardPile] = {}
    available = game.getAvailableCards(cardtype)
    # To make up the numbers
    for nkc in available:
        klass = game.card_mapping[cardtype][nkc]
        dest[nkc] = pileClass(nkc, klass)
    return dest


###########################################################################
def instantiate_non_kingdom_card(game: "Game", cardtype: str, card_name: str) -> Card:
    klass = game.card_mapping[cardtype][card_name]
    return klass()


###########################################################################
def check_card_requirements(game: "Game") -> None:
    """If any card we are playing requires another card (e.g. Curse) then
    ensure that is loaded as well"""

    check_cards = (
        list(game._cards.values())
        + list(game.events.values())
        + list(game.traits.values())
        + list(game.hexes)
        + list(game.boons)
        + list(game.landmarks.values())
    )
    if game.ally:
        check_cards.append(game.ally)

    for card in check_cards:
        check_card_requirement(game, card)

    if game.init[Keys.ALLIES] and not game.ally:
        print(f"Need to specify a Liaison as well as an Ally {game.init[Keys.ALLIES]}")
        sys.exit(1)


###########################################################################
def guess_card_name(game: "Game", name: str, prefix: str = "Card") -> Optional[str]:
    """Don't force the user to give the exact card name on the command
    line - maybe we can guess it"""
    available = game.getAvailableCards(prefix)
    if name in available:
        return name
    lower_name = name.lower()
    for card_name in available:
        if card_name.lower() == lower_name:
            return card_name
        newc = card_name.lower().replace("'", "")
        if newc.lower() == lower_name:
            return card_name
        newc = newc.replace(" ", "_")
        if newc == lower_name:
            return card_name
        newc = newc.replace(" ", "-")
        if newc == lower_name:
            return card_name
        newc = newc.replace(" ", "")
        if newc == lower_name:
            return card_name
        newc = newc.replace("_", "")
        if newc == lower_name:
            return card_name
    return None


###########################################################################
def good_names(game: "Game", specified: list[str], cardtype: str) -> list[str]:
    """Replace specified names with ones that are good"""
    answer: list[str] = []
    for name in specified:
        if name in game.card_mapping[cardtype]:
            answer.append(name)
        else:
            good_name = guess_card_name(game, name, cardtype)
            if good_name is None:
                sys.stderr.write(f"Unknown {cardtype} '{name}'\n")
                sys.exit(1)
            answer.append(good_name)
    return answer


###########################################################################
def load_non_kingdom_cards(
    game: "Game", cardtype: str, specified: list[str], num_required: Optional[int] = None
) -> dict[str, Card]:
    """Load non kingdom cards into the game
    If specific cards are required they need to be in `specified`
    Up to numrequired cards will be used

    Returns a dictionary; key is the name, value is the instance
    """
    dest: dict[str, Card] = {}
    available = game.getAvailableCards(cardtype)
    # Specified cards
    if specified is not None:
        names = good_names(game, specified, cardtype)
        for nkc in names:
            dest[nkc] = instantiate_non_kingdom_card(game, cardtype, nkc)
            available.remove(nkc)

    # To make up the numbers
    if num_required is not None:
        while len(dest) < num_required:
            nkc = random.choice(available)
            dest[nkc] = instantiate_non_kingdom_card(game, cardtype, nkc)
            available.remove(nkc)
    else:  # Do them all
        for nkc in available:
            dest[nkc] = instantiate_non_kingdom_card(game, cardtype, nkc)

    return dest


###########################################################################
def use_card_pile(
    game: "Game",
    available: list[str] | None,
    card_name: str,
    force: bool = False,
    card_type: str = "Card",
) -> int:
    """Set up a card pile for use
    Return 1 if it counts against the number of card piles in use"""
    try:
        if available is not None:
            available.remove(card_name)
    except ValueError:  # pragma: no cover
        print(f"Unknown card '{card_name}'\n", file=sys.stderr)
        sys.exit(1)
    card = game.card_mapping[card_type][card_name]()
    if not game.flags[Flags.ALLOW_POTIONS] and card.potcost:
        return 0
    if hasattr(card, "cardpile_setup"):
        card_pile = card.cardpile_setup(game)
    else:
        card_pile = CardPile(game)
    num_cards = num_cards_in_pile(game, card)
    card_pile.init_cards(num_cards, game.card_mapping[card_type][card_name])
    if not force and not card.insupply:
        return 0

    game.card_piles[card_name] = card_pile
    for card in card_pile:
        if card_name not in game.card_instances:
            game.card_instances[card_name] = game.card_mapping[card_type][card_name]()
        game._cards[card.uuid] = card
        if not card.pile:
            card.pile = card_name
        card.location = Piles.CARDPILE
    game.output(f"Playing with {card_name}")
    return 1


###########################################################################
def num_cards_in_pile(game: "Game", card: Card) -> int:
    """Return the number of cards that should be in a card pile"""
    if hasattr(card, "calc_numcards"):
        return card.calc_numcards(game)
    elif hasattr(card, "numcards"):
        return card.numcards
    else:
        return 10


###########################################################################
def load_decks(game: "Game", initcards: list[str], numstacks: int) -> None:
    """Determine what cards we are using this game"""
    for card in game._base_cards:
        use_card_pile(game, game._base_cards[:], card, force=True, card_type="BaseCard")
    available = game.getAvailableCards()
    unfilled = numstacks
    found_all = True
    for crd in initcards:
        # These cards get loaded by other things
        if crd in ("Boons", "Hexes"):
            continue
        result = place_init_card(game, crd, available)
        if result is None:
            found_all = False
        else:
            unfilled -= result

    if not found_all:
        sys.exit(1)

    while unfilled > 0:
        if not available:
            # Not enough cards to fill the hand - almost certainly in a test
            break
        crd = random.choice(available)
        if crd in game.init[Keys.BAD_CARDS]:
            continue
        unfilled -= use_card_pile(game, available, crd)

    check_card_requirements(game)


###########################################################################
def place_init_card(game: "Game", card: str, available: list[str]) -> Optional[int]:
    """For the specified card, load it into the correct deck
    Return the number of kingdom card piles used or None for not found
    """
    # If base cards are specified by initcards
    if card_name := guess_card_name(game, card, prefix="BaseCard"):
        use_card_pile(game, None, card_name, force=True, card_type="BaseCard")
        return 0
    if card_name := guess_card_name(game, card):
        return use_card_pile(game, available, card_name, force=True)
    if event_name := guess_card_name(game, card, "Event"):
        game.init[Keys.EVENT].append(event_name)
        return 0
    if way_name := guess_card_name(game, card, "Way"):
        game.init[Keys.WAY].append(way_name)
        return 0
    if landmark_name := guess_card_name(game, card, "Landmark"):
        game.init[Keys.LANDMARK].append(landmark_name)
        return 0
    if project_name := guess_card_name(game, card, "Project"):
        game.init[Keys.PROJECTS].append(project_name)
        return 0
    if ally_name := guess_card_name(game, card, "Ally"):
        game.init[Keys.ALLIES].append(ally_name)
        return 0
    if trait_name := guess_card_name(game, card, "Trait"):
        game.init[Keys.TRAITS].append(trait_name)
        return 0
    if guess_card_name(game, card, "Boon"):
        load_boons(game)
        return 0
    if guess_card_name(game, card, "Artifact"):
        # Artifacts should be loaded by the requiring card but can still be specified
        # in a card set
        return 0
    if card.lower() == "shelters":
        # Use of shelters handled elsewhere
        return 0
    # Cards that exist but are handled elsewhere
    for prefix in ("Traveller", "Castle", "Loot", "Heirloom", "State", "Hex", "PrizeCard"):
        if guess_card_name(game, card, prefix):
            return 0
    print(f"Can't guess what card '{card}' is")
    return None


###########################################################################
def setup_players(
    game: "Game",
    playernames: Optional[list[str]] = None,
    plr_class: type[Player] = TextPlayer,
) -> None:
    if use_shelters := use_shelters_in_game(game, game.flags[Flags.ALLOW_SHELTERS], game.init[Keys.CARDS]):
        setup_shelters(game)
    names = playerNames[:]
    if playernames is None:
        playernames = []

    for player_num in range(game.numplayers):
        try:
            name = playernames.pop()
        except IndexError:
            name = random.choice(names)
            names.remove(name)
        the_uuid = uuid.uuid4().hex
        if game.bot:
            game.players[the_uuid] = BotPlayer(
                game=game,
                quiet=game.quiet,
                name=f"{name}Bot",
                heirlooms=game.heirlooms,
                use_shelters=use_shelters,
            )
            game.bot = False
        elif game.randobot:
            game.players[the_uuid] = RandobotPlayer(
                game=game,
                quiet=game.quiet,
                name=f"{name}RandoBot",
                heirlooms=game.heirlooms,
                use_shelters=use_shelters,
            )
            game.randobot -= 1
        else:
            game.players[the_uuid] = plr_class(
                game=game,
                quiet=game.quiet,
                name=name,
                number=player_num,
                heirlooms=game.heirlooms,
                use_shelters=use_shelters,
            )
        game.players[the_uuid].uuid = the_uuid


# EOF
