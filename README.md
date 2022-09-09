[![Build Status](https://travis-ci.org/dwagon/pydominion.svg?branch=develop)](https://travis-ci.org/dwagon/pydominion)
[![Coverage Status](https://coveralls.io/repos/dwagon/pydominion/badge.png)](https://coveralls.io/r/dwagon/pydominion)

pydominion
==========

A simple version of an excellent game called dominion

Please buy the physical game: it is awesome fun

http://boardgamegeek.com/boardgame/36218/dominion

Usage
=====

Text interface

```
usage: Game.py [-h] [--numplayers NUMPLAYERS] [--card INITCARDS]
               [--bad BADCARDS] [--numevents NUMEVENTS] [--events EVENTCARDS]
               [--numlandmarks NUMLANDMARKS] [--landmark LANDMARKCARDS]
               [--cardset CARDSET] [--cardbase CARDBASE] [--cardpath CARDPATH]
               [--prosperity] [--bot] [--quiet]

Play dominion

optional arguments:
  -h, --help            show this help message and exit
  --numplayers NUMPLAYERS
                        How many players
  --card INITCARDS      Include card in lineup
  --bad BADCARDS        Do not include card in lineup
  --numevents NUMEVENTS
                        Number of events to use
  --events EVENTCARDS   Include event
  --numlandmarks NUMLANDMARKS
                        Number of landmarks to use
  --landmark LANDMARKCARDS
                        Include landmark
  --cardset CARDSET     File containing list of cards to use
  --cardbase CARDBASE   Include only cards from the specified base
  --cardpath CARDPATH   Where to find card definitions
  --prosperity          Use colonies and platinums
  --bot                 Bot Player
  --quiet               Supress a lot of output
```

To play a random game:
```
./Game.py
```

or try one of the official cardsets
```
./Game.py --cardset ../cardset/<cardset>
```

To play against a simple (and occassionally buggy) bot which implements the big money strategy, just add '--bot' to the args

images
======

Card images from http://wiki.dominionstrategy.com/ which is also a great resource for strategies and rule clarity
