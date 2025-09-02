"""Code relating to printing stuff for player prompts"""

import os
from typing import Optional, TYPE_CHECKING

from dominion import Limits, Piles, Phase, Card
from dominion.Option import Option
from dominion.PlayArea import PlayArea

if TYPE_CHECKING:
    from dominion.Player import Player


###########################################################################
def generate_prompt(player: "Player") -> str:
    """Return the prompt to give to the user"""
    status = f"Actions={player.actions.get()} Buys={player.buys.get()}"
    if player.coins:
        status += f" Coins={player.coins.get()}"
    if player.debt:
        status += f" Debt={player.debt.get()}"
    if player.potions:
        status += " Potion"
    if player.favors:
        status += f" Favours={player.favors.get()}"
    if player.coffers:
        status += f" Coffer={player.coffers.get()}"
    if player.villagers:
        status += f" Villager={player.villagers.get()}"
    if player.limits[Limits.PLAY] is not None:
        status += f" Play Limit={player.limits[Limits.PLAY]}"
    prompt = f"What to do ({status})?"
    return prompt


###########################################################################
def spendable_selection(player: "Player") -> list[Option]:
    options = []
    spendable = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
    spendable.sort(key=lambda x: x.name)
    total_coin = sum(player.hook_spend_value(_) for _ in spendable)
    numpots = sum(1 for _ in spendable if _.name == "Potion")
    potstr = f", {numpots} potions" if numpots else ""
    details = f"{total_coin} coin{potstr}"
    if spendable:
        o = Option(
            selector="1",
            verb="Spend all treasures",
            details=details,
            card=None,
            action="spendall",
        )
        options.append(o)

    if player.coffers:
        o = Option(selector="2", verb="Spend Coffer (1 coin)", card=None, action="coffer")
        options.append(o)

    if player.debt and player.coins:
        o = Option(selector="3", verb="Payback Debt", card=None, action="payback")
        options.append(o)

    index = 4
    for card in spendable:
        tp = f"{player.hook_spend_value(card)} coin; {card.get_cardtype_repr()}"
        o = Option(
            selector=str(index),
            name=card.name,
            details=tp,
            verb="Spend",
            card=card,
            action="spend",
            desc=card.description(player),
        )
        options.append(o)
        index += 1

    return options


###########################################################################
def get_all_purchasable(player) -> PlayArea:
    """Return all potentially purchasable cards"""
    all_cards = PlayArea("all_purchasable")
    for name, pile in player.game.get_card_piles():
        if pile.is_empty():
            continue
        card = pile.get_top_card()
        if card is None:
            continue
        if not card.purchasable:
            continue
        all_cards.add(card)
    all_cards.sort(key=player.card_cost)
    all_cards.sort(key=lambda x: x.basecard)
    return all_cards


###########################################################################
def buyable_selection(player: "Player", index: int) -> tuple[list[Option], int]:
    options = []
    all_cards = get_all_purchasable(player)
    buyable = player.cards_under(coin=player.coins.get(), num_potions=player.potions.get())
    for card in all_cards:
        if not player.hook_allowed_to_buy(card):
            if card in buyable:
                buyable.remove(card)
        sel = chr(ord("a") + index)
        if not player.debt and player.buys and card in buyable and card not in player.forbidden_to_buy:
            action = "buy"
            verb = "Buy"
        else:
            sel = "-"
            verb = ""
            action = None
        details = [player._cost_string(card)]
        if player.game.card_piles[card.pile].embargo_level:
            details.append(f"Embargo {player.game.card_piles[card.pile].embargo_level}")
        if player.game.card_piles[card.pile].getVP():
            details.append(f"Gathered {player.game.card_piles[card.name].getVP()} VP")
        details.append(card.get_cardtype_repr())
        details.append(f"{len(player.game.card_piles[card.pile])} left")
        for tkn in player.which_token(card.name):
            details.append(f"[Tkn: {tkn}]")
        o = Option(
            selector=sel,
            verb=verb,
            desc=card.description(player),
            name=card.name,
            details="; ".join(details),
            card=card,
            action=action,
        )
        options.append(o)
        index += 1
    return options, index


###########################################################################
def event_selection(player: "Player", index: int) -> tuple[list[Option], int]:
    """Generate player options for selecting events"""
    options = []
    for op in player.game.events.values():
        index += 1
        if op.cost <= player.coins.get() and player.buys and not player.debt:
            sel = chr(ord("a") + index)
            action = "event"
        else:
            sel = "-"
            action = None
        details = f"Event; {player._cost_string(op)}"
        o = Option(
            selector=sel,
            verb="Use",
            desc=op.description(player),
            name=op.name,
            details=details,
            card=op,
            action=action,
        )
        options.append(o)

    return options, index


###########################################################################
def project_selection(player: "Player", index: int) -> tuple[Optional[list[Option]], int]:
    """Allow player to select projects"""
    if not player.game.projects:
        return None, index
    # Can only have two projects
    if len(player.projects) == 2:
        return None, index
    options = []
    for op in player.game.projects.values():
        index += 1
        if (op.cost <= player.coins.get() and player.buys) and (op not in player.projects):
            sel = chr(ord("a") + index)
            action = "project"
        else:
            sel = "-"
            action = None
        details = f"Project; {player._cost_string(op)}"
        o = Option(
            selector=sel,
            verb="Buy",
            desc=op.description(player),
            name=op.name,
            details=details,
            card=op,
            action=action,
        )
        options.append(o)

    return options, index


###########################################################################
def reserve_selection(player: "Player", index: int) -> tuple[list[Option], int]:
    whens = player._get_whens()
    options = []
    for card in player.piles[Piles.RESERVE]:
        if not card.callable:
            continue
        if card.when not in whens:
            continue
        index += 1
        sel = chr(ord("a") + index)
        details = card.get_cardtype_repr()
        o = Option(
            selector=sel,
            name=card.name,
            verb="Call",
            details=details,
            card=card,
            action="reserve",
            desc=card.description(player),
        )
        options.append(o)

    return options, index


###########################################################################
def night_selection(player: "Player", index: int) -> tuple[list[Option], int]:
    options = []
    nights = [c for c in player.piles[Piles.HAND] if c.isNight()]
    if nights:
        for n in nights:
            sel = chr(ord("a") + index)
            details = n.get_cardtype_repr()
            o = Option(
                verb="Play",
                selector=sel,
                name=n.name,
                details=details,
                card=n,
                action="play",
                desc=n.description(player),
            )
            options.append(o)
            index += 1
    return options, index


###########################################################################
def playable_selection(player: "Player", index: int) -> tuple[list[Option], int]:
    options = []
    playable = [_ for _ in player.piles[Piles.HAND] if _.playable and _.isAction()]
    if player.villagers:
        o = Option(
            selector="1",
            verb="Spend Villager (1 action)",
            card=None,
            action="villager",
        )
        options.append(o)

    for card in playable:
        sel = chr(ord("a") + index)
        options.append(card_option(card, player, sel))
        index += 1
        for way in player.game.ways.values():
            sel = chr(ord("a") + index)
            o = Option(
                verb="Play",
                selector=sel,
                name=way.name,
                desc=f"{card.name}: {way.description(player)}",
                action="way",
                card=card,
                way=way,
            )
            options.append(o)
            index += 1
    shadows = [_ for _ in player.piles[Piles.DECK] if _.isShadow() and _.isAction()]
    for shadow in shadows:
        sel = chr(ord("a") + index)
        options.append(card_option(shadow, player, sel))
        index += 1
    return options, index


###########################################################################
def card_option(card: Card.Card, player: "Player", selector: str) -> Option:
    details = card.get_cardtype_repr()
    o = Option(
        verb="Play",
        selector=selector,
        name=card.name,
        desc=card.description(player).strip(),
        action="play",
        card=card,
        details=details,
    )
    notes = ""
    for tkn in player.which_token(card.name):
        notes += f"[Tkn: {tkn}]"
    o["notes"] = notes
    return o


###########################################################################
def choice_selection(player: "Player") -> list[Option]:
    index = 0
    o = Option(selector="0", verb="End Phase", card=None, action="quit")
    options: list[Option] = [o]

    if player.phase == Phase.ACTION:
        if player.actions or player.villagers:
            op_p, index = playable_selection(player, index)
            options.extend(op_p)

    if player.phase == Phase.BUY:
        op_s = spendable_selection(player)
        options.extend(op_s)
        op_b, index = buyable_selection(player, index)
        options.extend(op_b)
        op_e, index = event_selection(player, index)
        options.extend(op_e)
        op_pr, index = project_selection(player, index)
        if op_pr:
            options.extend(op_pr)

    if player.phase == Phase.NIGHT:
        op, index = night_selection(player, index)
        options.extend(op)

    if player.piles[Piles.RESERVE].size():
        op_r, index = reserve_selection(player, index)
        options.extend(op_r)

    return options


###########################################################################
def display_tokens(player: "Player") -> str:
    """Generate the overview display for tokens"""
    token_output = []
    for tkn, tkv in player.tokens.items():
        if tkv:
            token_output.append(f"{tkn}: {tkv}")
    if player.card_token:
        token_output.append("-1 Card")
    if player.coin_token:
        token_output.append("-1 Coin")
    if player.journey_token:
        token_output.append("Journey Faceup")
    else:
        token_output.append("Journey Facedown")
    return "; ".join(token_output)


###########################################################################
def display_overview(player: "Player") -> None:
    """Display turn summary overview to player"""
    player.output("\n")
    player.output("-" * 50)
    player.output(f"| Phase: {player.phase.name.title()}")
    for landmark in player.game.landmarks.values():
        player.output(f"| Landmark {landmark.name}: {landmark.description(player)}")
    player.output(f"| Tokens: {display_tokens(player)}")
    if player.game.inactive_prophecy and not player.game.prophecy:
        player.output(
            f"| Inactive Prophecy: {player.game.inactive_prophecy.name} ({player.game.sun_tokens} Sun Tokens)"
        )
    if player.game.prophecy:
        player.output(f"| Prophecy: {player.game.prophecy.name}: {player.game.prophecy.description(player)}")
    if player.states:
        player.output(f"| States: {', '.join([_.name for _ in player.states])}")
    if player.piles[Piles.DEFER]:
        player.output(f"| Defer: {', '.join([str(_) for _ in player.piles[Piles.DEFER]])}")
    if player.piles[Piles.DURATION]:
        player.output(f"| Duration: {', '.join([str(_) for _ in player.piles[Piles.DURATION]])}")
    if player.projects:
        player.output(f"| Project: {', '.join([p.name for p in player.projects])}")
    if player.piles[Piles.RESERVE]:
        player.output(f"| Reserve: {', '.join([str(_) for _ in player.piles[Piles.RESERVE]])}")
    if player.piles[Piles.HAND]:
        player.output(
            f"| Hand ({len(player.piles[Piles.HAND])}): {', '.join([str(_) for _ in player.piles[Piles.HAND]])}"
        )
    else:
        player.output("| Hand: <EMPTY>")
    if player.artifacts:
        player.output(f"| Artifacts: {', '.join([_.name for _ in player.artifacts])}")
    for trait_name, trait in player.game.traits.items():
        player.output(f"| Trait {trait_name} on {trait.card_pile}: {trait.desc}")
    if player.piles[Piles.EXILE]:
        player.output(f"| Exile: {', '.join([str(_) for _ in player.piles[Piles.EXILE]])}")
    if player.piles[Piles.PLAYED]:
        player.output(
            f"| Played ({len(player.piles[Piles.PLAYED])}): {', '.join([str(_) for _ in player.piles[Piles.PLAYED]])}"
        )
    else:
        player.output("| Played: <NONE>")
    if os.getenv("PYDOMINION_DEBUG"):
        player.output(
            f"| Deck ({len(player.piles[Piles.DECK])}): {', '.join([str(_) for _ in player.piles[Piles.DECK]])}"
        )
        player.output(f"| Cards Elsewhere: {player.secret_count}")
    else:
        player.output(f"| Deck Size: {len(player.piles[Piles.DECK])}")
    if player.game.ally:
        player.output(f"| Ally: {player.game.ally.name}: {player.game.ally.description(player)}")
    player.output(
        f"| Discard ({len(player.piles[Piles.DISCARD])}): {', '.join([str(_) for _ in player.piles[Piles.DISCARD]])}"
    )  # Debug
    player.output(
        f"| Trash ({len(player.game.trash_pile)}): {', '.join([str(_) for _ in player.game.trash_pile])}"
    )  # Debug
    player.output(f"| {player.piles[Piles.DISCARD].size()} cards in discard pile")
    player.output("-" * 50)


# EOF
