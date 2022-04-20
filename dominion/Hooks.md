In order to have a large number of the card effects work there are a number of hooks (growing daily).
These are generally invoked from Player.py and defined in the Card.py and over-ridden in each card as required.

special(game, player)
---------------------
Almost every card has this - it is what makes the cards special.
Called when the card is played during the action phase
* player - current player

night(game, player)
-------------------
In night cards only - called when the card is active during the night phase
* player - current player

hook_allowed_to_buy
----------------
This is called before any card is available to purchase.
It should return True if the card is available to be purchased, or False otherwise.

hook_buy_card
------------
This is called after a card has been purchased, and is invoked for
every card in the players hand.

hook_buy_this_card
------------------
This is called after this card has been purchased.

hook_all_players_buy_card
---------------
If any player buys a card call this for any card in everyone's duration pile


hook_discard_this_card
----------------------
This is called when this card is discarded.

hook_way_discard_this_card
--------------------------
This is called when a card that was played through a way

hook_spend_value(game, player, card)
-----------------------------------
This modifies how much coin value you get for spending the card and
is invoked for every card that has been played this turn.

Return the delta. So 0 for no change.

hook_allplayers_gain_card
---------------
If any player gains a card call this for any card in everyone's hand

hook_pre_buy
-----------
Fires off before the buy phase

hook_end_buy_phase
-----------
Fires off at the end of the buy phase

hook_gain_card(game, player, card)
-------------
This hook is triggered for every card in play when you gain
another card.
It returns a dictionary of modifiers.

Currently:
    destination - if set then put the card in the destination pile
    trash - if true then trash card instead of gaining card

hook_gain_this_card
-------------
This is triggered when the card is gained

hook_cleanup
------------
Triggered for every played card at the start of the cleanup phase

hook_coinvalue
--------------
How much this card is worth

hook_trashThisCard
--------------
Called just before the card is trashed

hook_trash_card
--------------
Called for every card in your hand just before a card is trashed

hook_call_reserve
--------------
Called when a card is pulled from the Reserve

hook_all_players_pre_action(game, player, owner, card)
----------------------------------------------------
Called before action cards are played.
* player - current player
* owner - owner of the card with the hook
* card - card with the hook
Returns None or a dictionary with keys:
    skip_card - if true then the benefits of the card is skipped

hook_post_action(game, player, card)
---------------
Called for every card in played + duration pile after an action has happened

hook_end_turn
------------
Called at the end of the players buy phase

hook_start_turn
--------------
Called at the start of a players turn

hook_cardCost
------------
Modifier to the cost of buying a card. This hook applies to buying another card.

hook_this_card_cost
-----------------
Modifier to the cost of buying this card.

hook_revealThisCard
-----------------
Called when a card is revealed

hook_end_of_game
----------------
Called at the end of the game if they are registered in player.end_of_game_cards[]

hook_overpay
------------
Overpaying for a card

setup(game)
-----------
Any setup required before the game starts, but after all the card piles and players have been setup

duration(game, player)
----------------------
Gets invoked for duration cards the next turn

hook_underAttack
----------------
Called if you get under attack

hook_pre_shuffle
---------------
Called just before the deck gets shuffled

hook_post_shuffle(game, player)
--------------------------------
Called after the deck got shuffled


#EOF
