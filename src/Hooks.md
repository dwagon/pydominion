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

hook_spendValue
---------------
This modifies how much gold value you get for spending the card and is invoked for every card that has been played this turn.

Return the delta. So 0 for no change.

hook_purchasedCard
------------------

hook_gainCard
-------------
This is triggered every time you gain a card from a cardpile.
It returns a dictionary of modifiers.

Currently:
    destination - if set then put the card in the destination pile
#EOF
