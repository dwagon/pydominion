#!/usr/bin/env python

import os
import Game
from GuiPlayer import GuiPlayer

from flask import Flask, jsonify

game = Game.Game(bot=True)
game.startGame(plrKlass=GuiPlayer)
app = Flask(__name__)


###############################################################################
@app.route('/endturn')
def end_turn():
    game.turn()
    return jsonify({})


###############################################################################
@app.route('/player/list')
def player_list():
    # Just return the human player for now
    human = [k for k, v in game.players.items() if isinstance(v, GuiPlayer)]
    return jsonify(human)


###############################################################################
@app.route('/player/<plrid>/inputs')
def player_input(plrid):
    print("game.players[%s]._inputs=%s" % (plrid, game.players[plrid]._inputs))
    try:
        inp = game.players[plrid]._inputs.pop()
    except IndexError:
        inp = ""
    return jsonify(inp)


###############################################################################
@app.route('/player/<plrid>/messages')
def player_messages(plrid):
    try:
        msg = game.players[plrid]._messages.pop()
    except IndexError:
        msg = ""
    return jsonify(msg)


###############################################################################
@app.route('/player/<plrid>/hand')
def player_hand(plrid):
    hand = [card.name for card in game.players[plrid].hand]
    return jsonify(hand)


###############################################################################
@app.route('/deck/list')
def decks_list():
    cps = list(game.cardpiles.keys())
    return jsonify(cps)


###############################################################################
@app.route('/card/<cardname>')
def card_info(cardname):
    ans = serialize_card(cardname)
    return jsonify(ans)


###############################################################################
def serialize_card(cardname):
    details = game[cardname]
    if details.image:
        imagefile = os.path.join('images', details.image)
    else:
        imagefile = os.path.join('images', '%s.jpg' % cardname.lower())
        if not os.path.exists(imagefile):
            imagefile = os.path.join('images', '%s.jpg' % cardname.lower().replace(' ', '_'))
            if not os.path.exists(imagefile):
                print("image %s doesn't exist" % imagefile)
                imagefile = None
    ans = {
        'numcards': details.numcards,
        'basecard': details.basecard,
        'image': imagefile,
        'purchasable': details.purchasable,
        'cost': details.cost
        }
    return ans

# EOF
