"""Build kingdom description text for LLM prompts."""

from __future__ import annotations

import random
from typing import Any


def _spin_up_game(kingdom_cards: list[str], **game_kwargs: Any):
    """Create a deterministic throw-away game to read card metadata.

    Uses ``num_stacks=len(kingdom_cards)`` so the engine doesn't fill
    remaining slots with random cards.
    """
    from dominion.Game import Game
    from dominion.BotPlayer import BotPlayer

    saved_state = random.getstate()
    random.seed(0)
    game = Game(
        initcards=kingdom_cards,
        numplayers=2,
        quiet=True,
        player_classes=[BotPlayer, BotPlayer],
        num_stacks=len(kingdom_cards),  # don't fill remaining slots randomly
        **game_kwargs,
    )
    game.start_game()
    random.setstate(saved_state)
    return game


def generate_random_kingdom(
    seed: int | None = None,
    **game_kwargs: Any,
) -> tuple[list[str], dict[str, Any]]:
    """Let the Dominion engine generate a fully random kingdom.

    Spins up a game with ``initcards=[]`` and ``num_stacks=10`` so the
    engine fills all 10 kingdom slots randomly.  After ``start_game()``,
    extracts the chosen kingdom card names and any resolved game_kwargs
    (prosperity, events, landmarks, etc.).

    Returns ``(kingdom_cards, effective_game_kwargs)`` — everything needed
    to reproduce the game deterministically.
    """
    from dominion.Game import Game
    from dominion.BotPlayer import BotPlayer

    if seed is not None:
        random.seed(seed)

    game = Game(
        initcards=[],
        numplayers=2,
        quiet=True,
        player_classes=[BotPlayer, BotPlayer],
        **game_kwargs,
    )
    game.start_game()

    # Extract kingdom cards (non-base piles that are actual purchasable kingdom cards)
    kingdom_cards: list[str] = []
    for pile_name, pile in game.card_piles.items():
        inst = game.card_instances.get(pile_name)
        if inst is None:
            continue
        if inst.basecard:
            continue
        # Skip non-purchasable special piles (Loot, Shelters, etc.)
        if not getattr(inst, "purchasable", True):
            continue
        kingdom_cards.append(pile_name)

    # Build effective game_kwargs that would reproduce this exact setup
    effective_kwargs: dict[str, Any] = dict(game_kwargs)  # start with explicit args

    # Capture implicit mechanics the engine loaded
    if "Colony" in game.card_piles and "prosperity" not in effective_kwargs:
        effective_kwargs["prosperity"] = True
    if game.events and "events" not in effective_kwargs:
        effective_kwargs["events"] = list(game.events.keys())
    if game.landmarks and "landmarks" not in effective_kwargs:
        effective_kwargs["landmarks"] = list(game.landmarks.keys())
    if game.ways and "ways" not in effective_kwargs:
        effective_kwargs["ways"] = list(game.ways.keys())
    if game.projects and "projects" not in effective_kwargs:
        effective_kwargs["projects"] = list(game.projects.keys())
    if game.traits and "traits" not in effective_kwargs:
        effective_kwargs["traits"] = list(game.traits.keys())
    if game.ally and "allies" not in effective_kwargs:
        effective_kwargs["allies"] = [game.ally.name]

    return kingdom_cards, effective_kwargs


def get_resolved_mechanics(
    kingdom_cards: list[str],
    **game_kwargs: Any,
) -> dict[str, Any]:
    """Return a dict describing all mechanics the engine resolved for this kingdom.

    This captures implicit mechanics (allies loaded by Liaison cards, boons
    loaded by Fate cards, etc.) that aren't part of the explicit game_kwargs
    but ARE active in the game.  Useful for config/reproducibility logging.
    """
    game = _spin_up_game(kingdom_cards, **game_kwargs)

    resolved: dict[str, Any] = {}

    if "Colony" in game.card_piles:
        resolved["prosperity"] = True
    if "Potion" in game.card_piles:
        resolved["potion"] = True
    if game.events:
        resolved["events"] = list(game.events.keys())
    if game.landmarks:
        resolved["landmarks"] = list(game.landmarks.keys())
    if game.ways:
        resolved["ways"] = list(game.ways.keys())
    if game.projects:
        resolved["projects"] = list(game.projects.keys())
    if game.traits:
        resolved["traits"] = {
            name: trait.card_pile for name, trait in game.traits.items()
        }
    if game.ally:
        resolved["ally"] = game.ally.name
    if game.inactive_prophecy:
        resolved["prophecy"] = game.inactive_prophecy.name
    all_boons = list(game.boons) + list(game.discarded_boons) + list(game.retained_boons)
    if all_boons:
        resolved["boons"] = sorted(set(b.name for b in all_boons))
    all_hexes = list(game.hexes) + list(game.discarded_hexes)
    if all_hexes:
        resolved["hexes"] = sorted(set(h.name for h in all_hexes))
    if game.artifacts:
        resolved["artifacts"] = list(game.artifacts.keys())
    loot_pile = game.card_piles.get("Loot")
    if loot_pile is not None and len(loot_pile) > 0:
        resolved["loot"] = sorted(set(c.name for c in loot_pile))

    return resolved


def get_kingdom_description(
    kingdom_cards: list[str],
    **game_kwargs: Any,
) -> str:
    """Build a text block describing the kingdom and all active mechanics.

    Spins up a temporary game just to read card metadata, then
    shuts it down immediately.  Extra ``game_kwargs`` are forwarded to
    the ``Game`` constructor so the caller can pass ``prosperity=True``,
    ``events=["Advance"]``, ``landmarks=["Aqueduct"]``, etc.

    Returns a formatted string suitable for inclusion in an LLM prompt.
    """
    game = _spin_up_game(kingdom_cards, **game_kwargs)

    lines: list[str] = []

    # ── Kingdom cards ──────────────────────────────────────────────
    lines.append("Kingdom Cards:")
    for name in kingdom_cards:
        card = game.card_instances.get(name)
        if card is None:
            lines.append(f"  {name} — (card not found in engine)")
            continue

        types: list[str] = []
        if card.isAction():
            types.append("Action")
        if card.isTreasure():
            types.append("Treasure")
        if card.isVictory():
            types.append("Victory")
        if card.isAttack():
            types.append("Attack")
        if card.isReaction():
            types.append("Reaction")

        type_str = ", ".join(types) if types else "?"
        lines.append(f"  {name} (${card.cost}) [{type_str}] — {card.desc}")

    # ── Standard supply ────────────────────────────────────────────
    lines.append("")
    supply_parts = [
        "Copper ($0, +1 coin)", "Silver ($3, +2 coins)", "Gold ($6, +3 coins)",
        "Estate ($2, 1VP)", "Duchy ($5, 3VP)", "Province ($8, 6VP)",
        "Curse ($0, -1VP)",
    ]

    has_colony = "Colony" in game.card_piles
    has_platinum = "Platinum" in game.card_piles
    if has_colony:
        supply_parts.append("Colony ($11, 10VP)")
    if has_platinum:
        supply_parts.append("Platinum ($9, +5 coins)")
    if "Potion" in game.card_piles:
        supply_parts.append("Potion ($4, produces potion for Alchemy cards)")

    lines.append("Standard supply also includes: " + ", ".join(supply_parts) + ".")

    if has_colony:
        lines.append(
            "Note: Colony is in play. The game also ends when the Colony pile is empty."
        )

    # ── Events ─────────────────────────────────────────────────────
    if game.events:
        lines.append("")
        lines.append("Events (pay the cost + spend 1 Buy to use instead of buying a card):")
        for name, event in game.events.items():
            lines.append(f"  {name} (${event.cost}) — {event.desc}")

    # ── Landmarks ──────────────────────────────────────────────────
    if game.landmarks:
        lines.append("")
        lines.append("Landmarks (passive scoring rules that affect all players):")
        for name, landmark in game.landmarks.items():
            desc = landmark.desc if landmark.desc else "(dynamic effect)"
            lines.append(f"  {name} — {desc}")

    # ── Ways ───────────────────────────────────────────────────────
    if game.ways:
        lines.append("")
        lines.append(
            "Ways (when you play an Action, you may use a Way's effect instead of the card's):"
        )
        for name, way in game.ways.items():
            lines.append(f"  {name} — {way.desc}")

    # ── Projects ───────────────────────────────────────────────────
    if game.projects:
        lines.append("")
        lines.append("Projects (one-time purchases that give permanent abilities):")
        for name, project in game.projects.items():
            lines.append(f"  {name} (${project.cost}) — {project.desc}")

    # ── Traits ─────────────────────────────────────────────────────
    if game.traits:
        lines.append("")
        lines.append("Traits (modify all cards in a specific supply pile):")
        for name, trait in game.traits.items():
            lines.append(f"  {name} (on {trait.card_pile} pile) — {trait.desc}")

    # ── Ally ───────────────────────────────────────────────────────
    if game.ally:
        lines.append("")
        lines.append(
            f"Ally: {game.ally.name} — {game.ally.desc}\n"
            f"  (Liaison cards give +1 Favor; spend Favors for the Ally's effect.)"
        )

    # ── Prophecy ───────────────────────────────────────────────────
    if game.inactive_prophecy:
        lines.append("")
        lines.append(
            f"Prophecy: {game.inactive_prophecy.name} — {game.inactive_prophecy.desc}\n"
            f"  (Omen cards remove Sun tokens; prophecy activates when tokens reach 0.)"
        )

    # ── Boons (from Fate cards) ────────────────────────────────────
    all_boons = list(game.boons) + list(game.discarded_boons) + list(game.retained_boons)
    if all_boons:
        lines.append("")
        lines.append("Boons (random positive effects received when you play a Fate card):")
        seen: set[str] = set()
        for boon in sorted(all_boons, key=lambda b: b.name):
            if boon.name not in seen:
                seen.add(boon.name)
                lines.append(f"  {boon.name} — {boon.desc}")

    # ── Hexes (from Doom cards) ────────────────────────────────────
    all_hexes = list(game.hexes) + list(game.discarded_hexes)
    if all_hexes:
        lines.append("")
        lines.append("Hexes (random negative effects inflicted by Doom cards):")
        seen_hex: set[str] = set()
        for hx in sorted(all_hexes, key=lambda h: h.name):
            if hx.name not in seen_hex:
                seen_hex.add(hx.name)
                lines.append(f"  {hx.name} — {hx.desc}")

    # ── Loot ───────────────────────────────────────────────────────
    loot_pile = game.card_piles.get("Loot")
    if loot_pile is not None and len(loot_pile) > 0:
        lines.append("")
        lines.append(
            "Loot (special treasures gained by card effects, not directly purchasable):"
        )
        # Loot pile is shuffled — list unique loot types
        seen_loot: set[str] = set()
        for card in loot_pile:
            if card.name not in seen_loot:
                seen_loot.add(card.name)
                lines.append(f"  {card.name} (${card.cost}) — {card.desc}")

    # ── Artifacts ──────────────────────────────────────────────────
    if game.artifacts:
        lines.append("")
        lines.append(
            "Artifacts (unique tokens claimed by specific cards; only one player holds each):"
        )
        for name, artifact in game.artifacts.items():
            lines.append(f"  {name} — {artifact.desc}")

    return "\n".join(lines)
