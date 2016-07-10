In order to have a large number of the card effects work there are a number of hooks (growing daily).
These are generally invoked from Player.py and defined in the Card.py and over-ridden in each card as required.

hook_allowedToBuy
----------------
This is called before any card is available to purchase.
It should return True if the card is available to be purchased, or False otherwise.

hook_buyCard
------------
This is called after a card has been purchased, and is invoked for
every card in the players hand.

hook_buyThisCard
------------
This is called after this card has been purchased.

hook_allPlayers_buyCard
---------------
If any player buys a card call this for any card in everyone's duration pile


hook_discardCard
----------------
This is called when this card is discarded.

hook_spendValue
---------------
This modifies how much coin value you get for spending the card and
is invoked for every card that has been played this turn.

Return the delta. So 0 for no change.

hook_allPlayers_gainCard
---------------
If any player gains a card call this for any card in everyone's hand

hook_preBuy
-----------
Fires off before the buy phase

hook_gainCard
-------------
This hook is triggered for every card in play when you gain
another card.
It returns a dictionary of modifiers.

Currently:
    destination - if set then put the card in the destination pile
    trash - if true then trash card instead of gaining card

hook_gainThisCard
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

hook_trashCard
--------------
Called for every card in your hand just before a card is trashed

hook_callReserve
--------------
Called when a card is pulled from the Reserve

hook_postAction
---------------
Called for every card in played + duration pile after an action has happened

hook_endTurn
------------
Called at the end of the players buy phase

hook_cardCost
------------
Modifier to the cost of buying a card. This hook applies to buying another card.

hook_thisCardCost
-----------------
Modifier to the cost of buying this card.

hook_end_of_game
----------------
Called at the end of the game if they are registered in player.end_of_game_cards[]

hook_overpay
------------
Overpaying for a card

setup
-----
Any setup required before the game starts, but after all the card piles and players have been setup

duration
--------
Gets invoked for duration cards the next turn

#EOF
