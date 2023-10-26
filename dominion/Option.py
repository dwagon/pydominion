""" Option Class"""
from typing import Optional, Any


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

    def __init__(self, **kwargs: Any) -> None:
        self.data: dict[str, Optional[Any]] = kwargs

    def __setitem__(self, key: str, value: str) -> None:
        self.data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __getitem__(self, key: str) -> Optional[Any]:
        if key == "print":
            raise Exception("print")
        return "" if key not in self.data else self.data[key]

    def __repr__(self) -> str:
        return f"<Option: {self.data}>"

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """dictionary.get()"""
        if key in self.data:
            return self[key]
        return default


# EOF
