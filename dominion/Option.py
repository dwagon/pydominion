class Option:
    """
     a) Buy Peasant (2 Coins; 9 left): +1 Buy, +1 Coin; Discard to replace with Soldier
     selector) verb name (details) desc
    selector = 'a'
    verb = 'Buy'
    desc = '+1 Buy, ...'
    name = 'Peasant'
    details = '2 Coins, ...'
    card = Card(Peasant)
    action = 'buy'
      or
    output = 'everything on one line'

    """

    def __init__(self, *args, **kwargs):
        self.msgs = args
        self.data = kwargs

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        if key == "print":
            raise Exception("print")
        if key not in self.data:
            return ""
        return self.data[key]

    def __repr__(self):
        return "<Option: %s>" % self.data


# EOF
