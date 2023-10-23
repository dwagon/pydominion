""" Counter - wrapped integer """
from typing import Any


###############################################################################
class Counter:
    """Counter - wrapped integer"""

    def __init__(self, name: str, value: int = 0):
        self._name = name
        self._value = value

    def get(self) -> int:
        """Get the value"""
        return self._value

    def set(self, value: int) -> int:
        """Set the value - for debugging"""
        self._value = value
        return self._value

    def add(self, mod: int) -> None:
        """Add to the value"""
        self._value += mod

    def __add__(self, obj: Any) -> "Counter":
        if isinstance(obj, int):
            self._value += obj
        elif hasattr(obj, "get"):
            self._value += obj.get()
        else:
            raise NotImplementedError(f"Counter __add__({obj=}) {type(obj)}")
        return Counter(self._name, self._value)

    def __sub__(self, obj: Any) -> "Counter":
        if isinstance(obj, int):
            self._value -= obj
        elif hasattr(obj, "get"):
            self._value -= obj.get()
        else:
            raise NotImplementedError(f"Counter __sub__({obj=}) {type(obj)}")
        return Counter(self._name, self._value)

    def __int__(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"<{self._name}={self._value}>"

    def __bool__(self) -> bool:
        return self._value != 0

    def __lt__(self, obj: Any) -> bool:
        if isinstance(obj, int):
            return self._value < obj
        elif hasattr(obj, "get"):
            return self._value < obj.get()
        raise NotImplementedError(f"Counter __sub__({obj=}) {type(obj)}")


# EOF
