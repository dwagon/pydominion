""" Counter - wrapped integer """


###############################################################################
class Counter:
    """Counter - wrapped integer"""

    def __init__(self, name: str, value: int = 0):
        self._name = name
        self._value = value

    def get(self) -> int:
        """Get the value"""
        return self._value

    def set(self, value) -> int:
        """Set the value - for debugging"""
        self._value = value
        return self._value

    def add(self, mod):
        """Add to the value"""
        self._value += mod

    def __add__(self, obj):
        if isinstance(obj, int):
            self._value += obj
        elif hasattr(obj, "get"):
            self._value += obj.get()
        else:
            raise NotImplementedError(f"Counter __add__({obj=}) {type(obj)}")
        return Counter(self._name, self._value)

    def __sub__(self, obj):
        if isinstance(obj, int):
            self._value -= obj
        elif hasattr(obj, "get"):
            self._value -= obj.get()
        else:
            raise NotImplementedError(f"Counter __sub__({obj=}) {type(obj)}")
        return Counter(self._name, self._value)

    def __repr__(self):
        return f"<{self._name}={self._value}>"

    def __bool__(self):
        return self._value != 0


# EOF
