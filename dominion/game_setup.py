"""Functions used to set up the game"""

import glob
import importlib
import os
import random
import sys
import uuid
from enum import StrEnum, auto
from typing import TYPE_CHECKING, cast, Optional, Any, Callable

from dominion import Keys
from dominion import Piles
from dominion.Artifact import Artifact
from dominion.Boon import BoonPile
from dominion.BotPlayer import BotPlayer
from dominion.Card import CardExpansion, Card
from dominion.CardPile import CardPile
from dominion.Event import Event
from dominion.Hex import HexPile, Hex
from dominion.Landmark import Landmark
from dominion.Loot import LootPile
from dominion.Names import playerNames
from dominion.Player import Player
from dominion.Project import Project
from dominion.Prophecy import Prophecy
from dominion.RandobotPlayer import RandobotPlayer
from dominion.TextPlayer import TextPlayer
from dominion.Trait import Trait
from dominion.Way import Way

if TYPE_CHECKING:  # pragma: no coverage
    from dominion.Game import Game


###########################################################################
class Flag(StrEnum):
    """Flags to control game setup behaviour"""

    ALLOW_POTIONS = auto()
    ALLOW_SHELTERS = auto()
    BOT = auto()
    LOADED_PRIZES = auto()
    LOADED_TRAVELLERS = auto()
    NUM_STACKS = auto()
    RANDOBOT = auto()
    USE_OLD_CARDS = auto()
    USE_PROSPERITY = auto()


BASE_CARDS = ["Copper", "Silver", "Gold", "Estate", "Duchy", "Province"]
PATHS: dict[Keys, str] = {}
INIT_NUMBERS: dict[Keys, int] = {}
INIT_CARDS: dict[Keys, list[Any]] = {}
INIT_OPTIONS: dict[Flag, Any] = {Flag.NUM_STACKS: 10, Flag.RANDOBOT: 0, Flag.BOT: False}
FLAGS: dict[Flag, bool] = {}


###########################################################################
def use_shelters_in_game(game: "Game", allow_shelters: bool, specified: list[str]) -> bool:
    """Should we use shelters"""
    if "shelters" in [_.lower() for _ in specified]:
        return True
    if not allow_shelters:
        return False

    # Pick a card to see if it is a dark ages card
    non_base_cards = [_ for _ in game.card_piles.keys() if not game.card_instances[_].basecard]
    card = game.card_instances[random.choice(non_base_cards)]
    if card.base == CardExpansion.DARKAGES:
        return True

    return False


###########################################################################
def setup_shelters(game: "Game") -> None:
    """Setup Shelters"""
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
    for way in ways:
        game.output(f"Playing with {way}")
    return cast(dict[str, Way], ways)


###########################################################################
def load_events(game: "Game", specified: list[str], num_required: int) -> dict[str, Event]:
    """Load required events"""
    events = load_non_kingdom_cards(
        game,
        cardtype="Event",
        specified=specified,
        num_required=num_required,
    )
    for event in events:
        game.output(f"Playing with Events: {event}")
    return cast(dict[str, Event], events)


###########################################################################
def load_hexes(game: "Game") -> list[Hex]:
    """Load Hexes into Pile"""
    game.output("Using hexes")
    d = load_non_kingdom_pile(game, "Hex", HexPile)
    return cast(list[Hex], list(d.values()))


###########################################################################
def load_projects(game: "Game", specified: list[str], num_required: int) -> dict[str, Project]:
    """Load and return Projects"""
    projects = load_non_kingdom_cards(
        game,
        "Project",
        specified,
        num_required,
    )
    if projects:
        for project in projects:
            game.output(f"Playing with Project: {project}")
    return cast(dict[str, Project], projects)


###########################################################################
def load_prophecies(game: "Game", specified: list[str]) -> Prophecy:
    """Load all the prophecies and return one"""
    prophecies = load_non_kingdom_cards(
        game,
        "Prophecies",
        specified,
        1,
    )
    prophecy = prophecies[list(prophecies.keys())[0]]
    return cast(Prophecy, prophecy)


###########################################################################
def load_artifacts(game: "Game") -> dict[str, Artifact]:
    """Load and return artifacts"""
    artifacts = load_non_kingdom_cards(game, "Artifact", [], None)
    game.output("Playing with Artifacts")
    return cast(dict[str, Artifact], artifacts)


###########################################################################
def load_landmarks(game: "Game", specified: list[str], num_required: int) -> dict[str, Landmark]:
    """Load required landmarks"""
    if landmarks := load_non_kingdom_cards(
        game,
        "Landmark",
        specified,
        num_required,
    ):
        for landmark in landmarks:
            game.output(f"Playing with Landmark: {landmark}")
    return cast(dict[str, Landmark], landmarks)


###########################################################################
def card_piles_for_trait(game: "Game") -> list[str]:
    """Return piles that are suitable for traits"""
    card_piles = []
    for pile in game.card_piles:
        if game.card_piles[pile].trait:
            continue
        if pile in BASE_CARDS:
            continue
        if pile in ("Loot",):
            continue
        card = game.card_instances[pile]
        if not card.purchasable:
            continue
        if not card.isAction() and not card.isTreasure():
            continue
        card_piles.append(pile)
    return card_piles


###########################################################################
def card_pile_for_trait(game: "Game", pile_selector: Callable[["Game"], list[str]] = card_piles_for_trait) -> str:
    """Return a card pile that is suitable for traits"""
    card_piles = pile_selector(game)
    card_pile = random.choice(card_piles)
    return card_pile


###########################################################################
def load_traits(
    game: "Game", specified: list[str], num_required: int, pile_picker: Callable[["Game"], str] = card_pile_for_trait
) -> None:
    """Load required Traits"""
    game.traits = cast(
        dict[str, Trait],
        load_non_kingdom_cards(
            game,
            cardtype="Trait",
            specified=specified,
            num_required=num_required,
        ),
    )
    for trait in game.traits:
        card_pile = pile_picker(game)
        game.assign_trait(trait, card_pile)
        game.output(f"Playing with Trait: {trait}")


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
def load_ally(game: "Game", specified: str | list[str]) -> Card:
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
def handle_specified_card_requirements(game: "Game", card: Card) -> None:
    """Look at the 'required_cards' value"""
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
            game.output(f"Using {card_name} as required by {card.name}")


###########################################################################
def check_heirloom_requirements(game: "Game", card: Card) -> None:
    """Check to see if heirlooms are required"""
    if card.heirloom is not None and card.heirloom not in game.heirlooms:
        use_card_pile(game, None, card.heirloom, force=True, card_type="Heirloom")
        game.heirlooms.append(card.heirloom)
        game.output(f"Using {card.heirloom} as required by {card.name}")


###########################################################################
def check_ruins_requirements(game: "Game", card: Card) -> None:
    """Check to see if ruins are required"""
    if card.isLooter() and "Ruins" not in game.card_piles:
        use_ruins(game)
        game.output(f"Using Ruins as required by {card.name}")


###########################################################################
def check_prize_requirements(game: "Game", card: Card) -> None:
    """Check to see if prizes are required"""
    if card.needs_prizes and not FLAGS[Flag.LOADED_PRIZES]:
        add_prizes(game)
        FLAGS[Flag.LOADED_PRIZES] = True
        game.output(f"Using Prizes as required by {card.name}")


###########################################################################
def check_artifact_requirements(game: "Game", card: Card) -> None:
    """Check to see if artifacts are required"""
    if card.needsartifacts and not game.artifacts:
        game.artifacts = load_artifacts(game)
        game.output(f"Using artifacts as required by {card.name}")


###########################################################################
def check_prophecy_requirements(game: "Game", card: Card) -> None:
    """Check to see if prophecies are required"""
    if card.isOmen() and not game.inactive_prophecy:
        game.inactive_prophecy = load_prophecies(game, INIT_CARDS[Keys.PROPHECIES])
        game.output(f"Playing with Prophecy {game.inactive_prophecy.name}")
        game.sun_tokens = get_num_sun_tokens(game)


###########################################################################
def check_project_requirements(game: "Game", card: Card) -> None:
    """Check to see if projects are required"""
    if card.needsprojects and not game.projects:
        game.projects = load_projects(game, INIT_CARDS[Keys.PROJECTS], INIT_NUMBERS[Keys.PROJECTS])
        game.output(f"Using projects as required by {card.name}")


###########################################################################
def check_allies_requirements(game: "Game", card: Card) -> None:
    """Check to see if allies are required"""
    if card.isLiaison() and not game.ally:
        game.ally = load_ally(game, INIT_CARDS[Keys.ALLIES])
        game.output(f"Using Allies as required by {card.name}")


###########################################################################
def check_traveller_requirements(game: "Game", card: Card) -> None:
    """Check to see if travellers are required"""
    if card.traveller and not FLAGS[Flag.LOADED_TRAVELLERS]:
        load_travellers(game)
        FLAGS[Flag.LOADED_TRAVELLERS] = True


###########################################################################
def check_boon_requirements(game: "Game", card: Card) -> None:
    """Check to see if boons are required"""
    if card.isFate() and not game.boons:
        load_boons(game)


###########################################################################
def check_hexes_requirements(game: "Game", card: Card) -> None:
    """Check to see if hexes are required"""
    if card.isDoom() and not game.hexes:
        game.hexes = load_hexes(game)
        game.output(f"Using hexes as required by {card.name}")


###########################################################################
def check_card_requirement(game: "Game", card: Card) -> None:
    """Ensure all the requirements (e.g. Curses) for a card are also loaded"""
    handle_specified_card_requirements(game, card)
    check_heirloom_requirements(game, card)
    check_ruins_requirements(game, card)
    check_prize_requirements(game, card)
    check_artifact_requirements(game, card)
    check_prophecy_requirements(game, card)
    check_project_requirements(game, card)
    check_traveller_requirements(game, card)
    check_allies_requirements(game, card)
    check_boon_requirements(game, card)
    check_hexes_requirements(game, card)


###########################################################################
def get_num_sun_tokens(game: "Game") -> int:
    """Return the number of sun tokens based on the number of players"""
    return {1: 3, 2: 5, 3: 8, 4: 10, 5: 12, 6: 13}[game.numplayers]


###########################################################################
def get_available_card_classes() -> dict[str, dict[str, type[Card]]]:
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
        mapping[prefix] = get_card_classes(prefix, PATHS[Keys.CARDS], "Card_")
        if FLAGS[Flag.USE_OLD_CARDS]:
            old_path = os.path.join(PATHS[Keys.CARDS], "old")
            mapping[prefix].update(get_card_classes(prefix, old_path, "Card_"))
    mapping["Event"] = get_card_classes("Event", PATHS[Keys.EVENT], "Event_")
    mapping["Way"] = get_card_classes("Way", PATHS[Keys.WAY], "Way_")
    mapping["Landmark"] = get_card_classes("Landmark", PATHS[Keys.LANDMARK], "Landmark_")
    mapping["Boon"] = get_card_classes("Boon", PATHS[Keys.BOONS], "Boon_")
    mapping["Hex"] = get_card_classes("Hex", PATHS[Keys.HEXES], "Hex_")
    mapping["State"] = get_card_classes("State", PATHS[Keys.STATES], "State_")
    mapping["Artifact"] = get_card_classes("Artifact", PATHS[Keys.ARTIFACTS], "Artifact_")
    mapping["Project"] = get_card_classes("Project", PATHS[Keys.PROJECTS], "Project_")
    mapping["Prophecies"] = get_card_classes("Prophecy", PATHS[Keys.PROPHECIES], "Prophecy_")
    mapping["Ally"] = get_card_classes("Ally", PATHS[Keys.ALLIES], "Ally_")
    mapping["Trait"] = get_card_classes("Trait", PATHS[Keys.TRAITS], "Trait_")
    mapping["Loot"] = get_card_classes("Loot", PATHS[Keys.LOOT], "Loot_")
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
    """Create an instance of a non-kingdom card so it can always be referenced for
    details."""
    klass = game.card_mapping[cardtype][card_name]
    return klass()


###########################################################################
def check_card_requirements(game: "Game") -> None:
    """If any card we are playing requires another card (e.g. Curse) then
    ensure that is loaded as well"""

    check_cards = (
        list(game.cards.values())
        + list(game.events.values())
        + list(game.traits.values())
        + list(game.hexes)
        + list(game.boons)
        + list(game.landmarks.values())
        + [game.inactive_prophecy]
    )
    if game.ally:
        check_cards.append(game.ally)

    for card in check_cards:
        if card is None:
            continue
        check_card_requirement(game, card)

    if INIT_CARDS[Keys.ALLIES] and not game.ally:
        print(f"Need to specify a Liaison as well as an Ally {INIT_CARDS[Keys.ALLIES]}")
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
    available: Optional[list[str]],
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
    if not FLAGS[Flag.ALLOW_POTIONS] and card.potcost:
        return 0
    if hasattr(card, "cardpile_setup"):
        card_pile = card.cardpile_setup(game)
    else:
        card_pile = CardPile(game)
    num_cards = num_cards_in_pile(game, card)
    card_pile.init_cards(num_cards, game.card_mapping[card_type][card_name])
    if not force and not card.insupply:
        return 0

    instantiate_card_pile(game, card_name, card_pile, card_type)

    game.output(f"Playing with {card_name}")
    return 1


###########################################################################
def instantiate_card_pile(game: "Game", card_name: str, card_pile: CardPile, card_type: str) -> None:
    """Create cards in the card pile"""
    game.card_piles[card_name] = card_pile
    for card in card_pile:
        if card_name not in game.card_instances:
            game.card_instances[card_name] = game.card_mapping[card_type][card_name]()
        game.cards[card.uuid] = card
        if not card.pile:
            card.pile = card_name
        card.location = Piles.CARDPILE


###########################################################################
def num_cards_in_pile(game: "Game", card: Card) -> int:
    """Return the number of cards that should be in a card pile"""
    if hasattr(card, "calc_numcards"):
        return card.calc_numcards(game)
    if hasattr(card, "numcards"):
        return card.numcards
    return 10


###########################################################################
def load_decks(game: "Game", initcards: list[str], numstacks: int) -> None:
    """Determine what cards we are using this game"""
    if FLAGS[Flag.USE_PROSPERITY]:
        BASE_CARDS.append("Colony")
        BASE_CARDS.append("Platinum")
    for card in BASE_CARDS:
        use_card_pile(game, BASE_CARDS[:], card, force=True, card_type="BaseCard")
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
        if crd in INIT_CARDS[Keys.BAD_CARDS]:
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
        INIT_CARDS[Keys.EVENT].append(event_name)
        return 0
    if way_name := guess_card_name(game, card, "Way"):
        INIT_CARDS[Keys.WAY].append(way_name)
        return 0
    if landmark_name := guess_card_name(game, card, "Landmark"):
        INIT_CARDS[Keys.LANDMARK].append(landmark_name)
        return 0
    if project_name := guess_card_name(game, card, "Project"):
        INIT_CARDS[Keys.PROJECTS].append(project_name)
        return 0
    if ally_name := guess_card_name(game, card, "Ally"):
        INIT_CARDS[Keys.ALLIES].append(ally_name)
        return 0
    if trait_name := guess_card_name(game, card, "Trait"):
        INIT_CARDS[Keys.TRAITS].append(trait_name)
        return 0
    if guess_card_name(game, card, "Boon"):
        load_boons(game)
        return 0
    if guess_card_name(game, card, "Artifact"):
        # Artifacts should be loaded by the requiring card but can still be specified
        # in a card set
        return 0
    if prophecy_name := guess_card_name(game, card, "Prophecies"):
        INIT_CARDS[Keys.PROPHECIES].append(prophecy_name)
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
def instantiate_player_class(game: "Game", name: str, use_shelters: bool, player_num: int, the_uuid: str) -> Player:
    """Create the player instances"""
    if INIT_OPTIONS[Flag.BOT]:
        plr_class: type[Player] = BotPlayer
        name = f"{name}Bot"
        INIT_OPTIONS[Flag.BOT] = False
    elif INIT_OPTIONS[Flag.RANDOBOT]:
        plr_class = RandobotPlayer
        name = f"{name}RandoBot"
        INIT_OPTIONS[Flag.RANDOBOT] -= 1
    else:
        plr_class = TextPlayer

    player = plr_class(
        game=game,
        quiet=game.quiet,
        name=name,
        heirlooms=game.heirlooms,
        use_shelters=use_shelters,
        number=player_num,
    )
    player.uuid = the_uuid
    return player


###########################################################################
def setup_players(
    game: "Game",
    use_shelters: bool,
    playernames: Optional[list[str]] = None,
) -> None:
    """Set up the players"""

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
        game.players[the_uuid] = instantiate_player_class(game, name, use_shelters, player_num, the_uuid)


###########################################################################
def parse_args(game: "Game", **args: Any) -> None:
    """Parse the arguments passed to the class"""
    PATHS[Keys.ALLIES] = args.get("ally_path", "dominion/allies")
    PATHS[Keys.ARTIFACTS] = args.get("artifact_path", "dominion/artifacts")
    PATHS[Keys.BOONS] = args.get("boon_path", "dominion/boons")
    PATHS[Keys.CARDS] = args.get("card_path", "dominion/cards")
    PATHS[Keys.EVENT] = args.get("event_path", "dominion/events")
    PATHS[Keys.HEXES] = args.get("hex_path", "dominion/hexes")
    PATHS[Keys.LANDMARK] = args.get("landmark_path", "dominion/landmarks")
    PATHS[Keys.LOOT] = args.get("loot_path", "dominion/loot")
    PATHS[Keys.PROJECTS] = args.get("project_path", "dominion/projects")
    PATHS[Keys.PROPHECIES] = args.get("prophecies_path", "dominion/prophecies")
    PATHS[Keys.STATES] = args.get("state_path", "dominion/states")
    PATHS[Keys.TRAITS] = args.get("trait_path", "dominion/traits")
    PATHS[Keys.WAY] = args.get("way_path", "dominion/ways")

    INIT_NUMBERS[Keys.EVENT] = args.get("num_events", 0)
    INIT_NUMBERS[Keys.LANDMARK] = args.get("num_landmarks", 0)
    INIT_NUMBERS[Keys.PROJECTS] = args.get("num_projects", 0)
    INIT_NUMBERS[Keys.TRAITS] = args.get("num_traits", 0)
    INIT_NUMBERS[Keys.WAY] = args.get("num_ways", 0)

    INIT_CARDS[Keys.ALLIES] = args.get("allies", [])
    INIT_CARDS[Keys.BAD_CARDS] = args.get("badcards", [])
    INIT_CARDS[Keys.CARDS] = args.get("initcards", [])
    INIT_CARDS[Keys.EVENT] = args.get("events", [])
    INIT_CARDS[Keys.LANDMARK] = args.get("landmarks", [])
    INIT_CARDS[Keys.PROJECTS] = args.get("projects", [])
    INIT_CARDS[Keys.PROPHECIES] = args.get("prophecies", [])
    if "prophecies" not in args:  # pragma: no coverage
        INIT_CARDS[Keys.PROPHECIES] = args.get("prophecy", [])
    INIT_CARDS[Keys.TRAITS] = args.get("traits", [])
    INIT_CARDS[Keys.WAY] = args.get("ways", [])

    INIT_OPTIONS[Flag.NUM_STACKS] = args.get("num_stacks", 10)
    FLAGS[Flag.ALLOW_POTIONS] = args.get("potions", True)
    FLAGS[Flag.USE_PROSPERITY] = args.get("prosperity", False)
    FLAGS[Flag.USE_OLD_CARDS] = args.get("oldcards", False)
    game.quiet = args.get("quiet", False)
    game.numplayers = args.get("numplayers", 2)
    INIT_OPTIONS[Flag.BOT] = args.get("bot", False)
    INIT_OPTIONS[Flag.RANDOBOT] = args.get("randobot", 0)
    FLAGS[Flag.ALLOW_SHELTERS] = args.get("shelters", True)


###########################################################################
def card_setup(game: "Game") -> None:
    """Run the setup() method for all cards"""
    for _, card_pile in list(game.card_piles.items()):
        card_pile.setup(game=game)
    for landmark in list(game.landmarks.values()):
        landmark.setup(game=game)
    for event in game.events.values():
        event.setup(game=game)
    if game.inactive_prophecy:
        game.inactive_prophecy.setup(game=game)


###########################################################################
def start_game(
    game: "Game",
    player_names: Optional[list[str]] = None,
) -> None:
    """Initialise game bits"""
    FLAGS[Flag.LOADED_TRAVELLERS] = False
    FLAGS[Flag.LOADED_PRIZES] = False

    load_decks(game, INIT_CARDS[Keys.CARDS], INIT_OPTIONS[Flag.NUM_STACKS])
    game.events = load_events(game, INIT_CARDS[Keys.EVENT], INIT_NUMBERS[Keys.EVENT])
    game.ways = load_ways(game, INIT_CARDS[Keys.WAY], INIT_NUMBERS[Keys.WAY])
    game.landmarks = load_landmarks(game, INIT_CARDS[Keys.LANDMARK], INIT_NUMBERS[Keys.LANDMARK])
    game.artifacts = load_artifacts(game)
    game.projects = load_projects(game, INIT_CARDS[Keys.PROJECTS], INIT_NUMBERS[Keys.PROJECTS])
    load_traits(game, INIT_CARDS[Keys.TRAITS], INIT_NUMBERS[Keys.TRAITS])

    if game.hexes or game.boons:
        load_states(game)
    check_card_requirements(game)
    if use_shelters := use_shelters_in_game(game, FLAGS[Flag.ALLOW_SHELTERS], INIT_CARDS[Keys.CARDS]):
        setup_shelters(game)
    setup_players(game, use_shelters, player_names)
    card_setup(game)  # Has to be after players have been created
    check_card_requirements(game)  # Again as setup can add requirements
    if game.hexes or game.boons:
        load_states(game)
    game.current_player = game.player_list()[0]
    if game.ally:
        for plr in game.player_list():
            plr.favors.add(1)
    game.save_original()


# EOF
