"""Chapel-based engine for the Village/Smithy/Witch kingdom.

Kingdom: Chapel, Village, Smithy, Market, Militia, Moat, Festival, Laboratory, Workshop, Witch

Strategy:
  1. Open Chapel + Silver. Chapel is the strongest $2 card in Dominion.
  2. Trash aggressively: Curses > Estates > Coppers (keep 2-3 Coppers early,
     then trash down to 0 once we have Silver/Gold income).
  3. Get one Witch early for the Curse attack — each Curse is -1 VP and bloats
     the opponent's deck. Two Witches is fine if Curses are still plentiful.
  4. Build a thin engine: Village (actions) + Laboratory/Smithy (draw) +
     Festival/Market (coins + buys). Prefer Laboratory over Smithy since Lab
     doesn't cost an action.
  5. Transition to Gold/Province once economy is strong. With a thin deck
     you reliably hit $8.
  6. Endgame: buy Duchy at $5 when Provinces <= 4, buy Estate at $2 when
     Provinces <= 2.
"""

from tournament.heuristic_player import HeuristicPlayer, BuyState, ActionState, TrashState, DiscardState, GainState
from typing import Optional


class ChapelEngine(HeuristicPlayer):
    """Chapel-based engine — thin deck, Witch attack, Village/draw engine."""

    # -- helpers --

    def _count(self, deck: dict[str, int], *names: str) -> int:
        return sum(deck.get(n, 0) for n in names)

    def _total_treasure_value(self, deck: dict[str, int]) -> int:
        return (deck.get("Copper", 0) * 1
                + deck.get("Silver", 0) * 2
                + deck.get("Gold", 0) * 3)

    def _total_actions(self, deck: dict[str, int]) -> int:
        return self._count(deck, "Chapel", "Village", "Smithy", "Market",
                           "Militia", "Moat", "Festival", "Laboratory",
                           "Workshop", "Witch")

    def _total_villages(self, deck: dict[str, int]) -> int:
        """Cards that give +2 actions (net +1 action)."""
        return self._count(deck, "Village", "Festival")

    def _total_terminals(self, deck: dict[str, int]) -> int:
        """Action cards that don't give +action (terminal actions)."""
        return self._count(deck, "Chapel", "Smithy", "Militia", "Moat",
                           "Workshop", "Witch")

    def _total_draw(self, deck: dict[str, int]) -> int:
        """Cards that draw cards."""
        return self._count(deck, "Smithy", "Laboratory", "Moat", "Witch", "Market")

    # -- buy phase --

    def buy_priority(self, state: BuyState) -> Optional[str]:
        coins = state.coins
        deck = state.my_deck
        provinces_left = state.provinces_remaining
        buyable = state.buyable

        # --- Endgame VP buying ---
        if coins >= 8 and "Province" in buyable:
            return "Province"

        # Late game duchies
        if coins >= 5 and provinces_left <= 4 and "Duchy" in buyable:
            return "Duchy"

        # Very late game estates
        if coins >= 2 and provinces_left <= 2 and "Estate" in buyable:
            return "Estate"

        # --- Opening (turns 1-2) ---
        if state.turn_number <= 2:
            if "Chapel" not in deck and "Chapel" in buyable:
                return "Chapel"
            if coins >= 3 and "Silver" in buyable:
                return "Silver"
            if coins == 2 and "Moat" in buyable:
                return "Moat"
            return None

        # --- Early game: get Chapel if we still don't have one ---
        if deck.get("Chapel", 0) == 0 and "Chapel" in buyable and coins >= 2:
            return "Chapel"

        # --- Witch priority: get 1-2 Witches while Curses remain ---
        curses_in_supply = state.supply.get("Curse")
        curses_remaining = curses_in_supply.remaining if curses_in_supply else 0

        if (coins >= 5 and "Witch" in buyable
                and deck.get("Witch", 0) < 2
                and curses_remaining >= 4):
            return "Witch"

        # --- Engine building ---
        villages = self._total_villages(deck)
        terminals = self._total_terminals(deck)
        draw_cards = self._total_draw(deck)

        # We need villages to support terminals. Rule of thumb:
        # want villages >= terminals - 1 (the first terminal is free)
        need_village = villages < terminals - 1

        if coins >= 5:
            # Laboratory is the best $5 — it's non-terminal draw
            if "Laboratory" in buyable and draw_cards < 4:
                return "Laboratory"

            # Festival gives +2 actions, +1 buy, +2 coins — great village
            if "Festival" in buyable and need_village:
                return "Festival"

            # Market is a cantrip with +coin +buy — always decent
            if "Market" in buyable and draw_cards >= 2:
                return "Market"

            # Gold if we have enough engine
            if "Gold" in buyable:
                return "Gold"

        if coins >= 4:
            # Militia is good early — +$2 and disrupts opponent
            if ("Militia" in buyable and deck.get("Militia", 0) == 0
                    and not need_village):
                return "Militia"

            # Smithy for draw if we have village support
            if "Smithy" in buyable and not need_village and draw_cards < 3:
                return "Smithy"

        if coins >= 3:
            # Village if we need action support
            if "Village" in buyable and need_village:
                return "Village"

            # Silver as fallback economy
            if "Silver" in buyable:
                return "Silver"

        # Don't buy junk at $1-2 mid-game
        return None

    # -- action phase --

    def action_priority(self, state: ActionState) -> Optional[str]:
        playable = state.playable_actions
        if not playable:
            return None

        hand = state.hand
        deck = state.my_deck
        actions = state.actions

        # --- Always play Chapel when we have junk to trash ---
        if "Chapel" in playable:
            junk = [c for c in hand if c in ("Curse", "Estate", "Copper")]
            # Trash Coppers if we have enough other economy
            copper_count = deck.get("Copper", 0)
            silver_plus = deck.get("Silver", 0) + deck.get("Gold", 0)
            # Keep a few coppers early, trash aggressively once we have economy
            if junk:
                # Don't "waste" Chapel if the only junk is Coppers and we still need them
                non_copper_junk = [c for c in junk if c != "Copper"]
                if non_copper_junk:
                    return "Chapel"
                # Trash coppers once we have 2+ silver/gold
                if silver_plus >= 2 and copper_count > 0:
                    return "Chapel"

        # --- Play villages before terminals (need actions) ---
        # If we only have 1 action, play a village first to unlock terminals
        if actions == 1:
            if "Festival" in playable:
                return "Festival"
            if "Village" in playable:
                return "Village"

        # --- Non-terminal draw ---
        if "Laboratory" in playable:
            return "Laboratory"
        if "Market" in playable:
            return "Market"

        # --- With actions to spare, play terminals ---
        if actions >= 2 or self._count_villages_in_hand(playable) > 0:
            if "Witch" in playable:
                return "Witch"
            if "Smithy" in playable:
                return "Smithy"
            if "Militia" in playable:
                return "Militia"
            if "Moat" in playable:
                return "Moat"
            if "Workshop" in playable:
                return "Workshop"

        # --- If only 1 action left, play best terminal ---
        if "Witch" in playable:
            return "Witch"
        if "Smithy" in playable:
            return "Smithy"
        if "Militia" in playable:
            return "Militia"
        if "Moat" in playable:
            return "Moat"

        # Play any remaining village
        if "Festival" in playable:
            return "Festival"
        if "Village" in playable:
            return "Village"

        return None

    def _count_villages_in_hand(self, playable: list[str]) -> int:
        return playable.count("Village") + playable.count("Festival")

    # -- trash phase ---

    def trash_priority(self, card_names: list[str], num: int, state: TrashState) -> list[str]:
        deck = state.my_deck
        silver_plus = deck.get("Silver", 0) + deck.get("Gold", 0)

        result: list[str] = []
        available = list(card_names)

        # Priority order: Curse > Estate > Copper (conditional)
        for target in ["Curse", "Estate"]:
            while target in available and len(result) < num:
                available.remove(target)
                result.append(target)

        # Trash Coppers aggressively once we have economy
        # Keep at most 2 Coppers early, then trash all
        coppers_in_deck = deck.get("Copper", 0)
        keep_coppers = 0 if silver_plus >= 3 else 2

        while "Copper" in available and len(result) < num and coppers_in_deck > keep_coppers:
            available.remove("Copper")
            result.append("Copper")
            coppers_in_deck -= 1

        return result

    # -- discard phase --

    def discard_priority(self, card_names: list[str], num: int, state: DiscardState) -> list[str]:
        # Discard priority: Curse > Estate > Duchy > Copper > Workshop > Chapel > others
        priority_order = ["Curse", "Estate", "Duchy", "Copper", "Workshop", "Chapel"]
        result: list[str] = []
        available = list(card_names)

        for target in priority_order:
            while target in available and len(result) < num:
                available.remove(target)
                result.append(target)

        # Fill remaining from whatever's left
        for name in available:
            if len(result) >= num:
                break
            result.append(name)

        return result[:num]

    # -- gain phase (Workshop, etc.) --

    def gain_priority(self, max_cost: int, state: GainState) -> Optional[str]:
        deck = state.my_deck
        gainable = state.gainable

        # With Workshop (gain up to $4):
        # Priority: Silver > Village (if needed) > Smithy (if needed)
        villages = self._total_villages(deck)
        terminals = self._total_terminals(deck)
        need_village = villages < terminals - 1

        if max_cost >= 4:
            if "Smithy" in gainable and not need_village and self._total_draw(deck) < 3:
                return "Smithy"

        if max_cost >= 3:
            if "Village" in gainable and need_village:
                return "Village"
            if "Silver" in gainable:
                return "Silver"

        return None
