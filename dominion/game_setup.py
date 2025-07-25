"""Functions used to set up the game"""

import glob
import importlib
import os
import random
from typing import TYPE_CHECKING, cast

from dominion.Boon import BoonPile
from dominion.Card import CardExpansion, Card
from dominion.CardPile import CardPile
from dominion.Event import Event
from dominion.Hex import HexPile
from dominion.Landmark import Landmark
from dominion.Loot import LootPile
from dominion.Way import Way

if TYPE_CHECKING:  # pragma: no coverage
    from dominion.Game import Game


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
        game.use_card_pile(None, trav, True, "Traveller")


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
    ways = game.load_non_kingdom_cards(
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
    events = game.load_non_kingdom_cards(
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
    d = game.load_non_kingdom_pile("Hex", HexPile)
    game.hexes = list(d.values())
    random.shuffle(game.hexes)


###########################################################################
def load_projects(game: "Game", specified: list[str], num_required: int) -> None:
    """TODO"""
    if game.projects:
        return
    game.projects = game.load_non_kingdom_cards(
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
    game.artifacts = game.load_non_kingdom_cards("Artifact", [], None)
    game.output("Playing with Artifacts")


###########################################################################
def load_landmarks(game: "Game", specified: list[str], num_required: int) -> dict[str, Landmark]:
    """Load required landmarks"""
    landmarks = game.load_non_kingdom_cards(
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
    game.traits = game.load_non_kingdom_cards(
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
    game.states = game.load_non_kingdom_cards("State", [], None)


###########################################################################
def load_boons(game: "Game") -> None:
    """Load boons into Pile"""
    if game.boons:
        return
    game.output("Using boons")
    d = game.load_non_kingdom_pile("Boon", BoonPile)
    game.boons = list(d.values())
    random.shuffle(game.boons)


###########################################################################
def load_ally(game: "Game", specified: list[str]) -> Card:
    """Load the ally"""
    if isinstance(specified, str):
        specified = [specified]
    allies = game.load_non_kingdom_cards("Ally", specified, 1)
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


# EOF
