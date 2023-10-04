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
usage: rungame.py [-h] [--numplayers NUMPLAYERS] [--card INITCARDS] [--bad BADCARDS] [--shelters SHELTERS] [--num_events NUM_EVENTS] [--events EVENTS]
                  [--num_ways NUM_WAYS] [--ways WAYS] [--num_landmarks NUM_LANDMARKS] [--landmark LANDMARKS] [--num_projects NUM_PROJECTS]
                  [--num_traits NUM_TRAITS] [--oldcards] [--project INIT_PROJECTS] [--ally ALLIES] [--trait TRAITS] [--cardset CARDSET] [--cardbase CARDBASE]
                  [--card_path CARD_PATH] [--prosperity] [--bot] [--randobot RANDOBOT] [--quiet]

Play dominion

options:
  -h, --help            show this help message and exit
  --numplayers NUMPLAYERS
                        How many players
  --card INITCARDS      Include card in lineup
  --bad BADCARDS        Do not include card in lineup
  --shelters SHELTERS   Allow shelters
  --num_events NUM_EVENTS
                        Number of events to use
  --events EVENTS       Include event
  --num_ways NUM_WAYS   Number of ways to use
  --ways WAYS           Include way
  --num_landmarks NUM_LANDMARKS
                        Number of landmarks to use
  --landmark LANDMARKS  Include landmark
  --num_projects NUM_PROJECTS
                        Number of projects to use
  --num_traits NUM_TRAITS
                        Number of traits to use
  --oldcards            Use cards from retired versions
  --project INIT_PROJECTS
                        Include project
  --ally ALLIES         Include specific ally
  --trait TRAITS        Include specific trait
  --cardset CARDSET     File containing list of cards to use
  --cardbase CARDBASE   Include only cards from the specified base
  --card_path CARD_PATH
                        Where to find card definitions
  --prosperity          Use colonies and platinum coins
  --bot                 Bot Player
  --randobot RANDOBOT   Number of Rando Bot Players
  --quiet               Supress a lot of output
```

To play a random game:
```
./dominion/rungame.py
```

or try one of the official cardsets
```
./dominion/rungame.py --cardset ../cardset/<cardset>
```

To play against a simple (and occasionally buggy) bot which implements the big money strategy, just add '--bot' to the args

images
======

Card images from http://wiki.dominionstrategy.com/ which is also a great resource for strategies and rule clarity
