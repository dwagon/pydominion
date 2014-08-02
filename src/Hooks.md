In order to have a large number of the card effects work there are a number of hooks (growing daily).
These are generally invoked from Player.py and defined in the Card.py and over-ridden in each card as required.

hook_allowedToBuy
----------------
This is called before any card is available to purchase.
It should return True if the card is available to be purchased, or False otherwise.

hook_buyCard
------------
This is called after a card has been purchased, and is invoked for every card in the players hand.

hook_discardCard
----------------
This is called when this card is discarded.

hook_spendValue
---------------
This modifies how much coin value you get for spending the card and is invoked for every card that has been played this turn.

Return the delta. So 0 for no change.

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

hook_coinvalue
--------------
How much this card is worth

hook_trashThisCard
--------------
Called just before the card is trashed

setup
-----
Any setup required before the game starts, but after all the card piles and players have been setup

duration
--------
Gets invoked for duration cards the next turn

#EOF
