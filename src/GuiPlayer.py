from Player import Player


###############################################################################
class GuiPlayer(Player):
    def __init__(self, game, name='', quiet=False, **kwargs):
        self._messages = []
        self._inputs = []
        Player.__init__(self, game, name)

    def plrChooseOptions(self, prompt, *choices):
        print("plrChooseOptions(prompt=%s, choices=%s)" % (prompt, str(choices)))

    def cardSel(self, num=1, **kwargs):
        print("cardSel(num=%d, kwargs=%s)" % (num, str(kwargs)))

    def userInput(self, options, prompt):
        print("userInput(options=%s, prompt=%s)" % (str(options), str(prompt)))
        self._inputs.append((options, prompt))

    def output(self, msg, end='\n'):
        self._messages.append(msg)

# EOF
