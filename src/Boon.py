from Card import Card


class Boon(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retain_boon = False


# EOF
