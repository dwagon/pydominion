#!/usr/bin/env python
""" Report on missing cards from wiki.dominionstrategy.com """
import subprocess
from typing import Any
import requests


##############################################################################
def get_html_data(url: str, request: dict[str, Any]) -> Any:
    """Get the HTML from the url"""
    lastContinue: dict[str, str] = {}

    while True:
        req = request.copy()  # Clone original requestd
        req.update(lastContinue)
        result = requests.get(url, params=req).json()
        if "error" in result:
            raise Exception(result["error"])
        if "warnings" in result:
            print(result["warnings"])
        if "query" in result:
            yield result["query"]
        if "query-continue" not in result:
            break
        lastContinue = result["query-continue"]["categorymembers"]


##############################################################################
def validate_card(card_name: str) -> bool:
    """Validate if this card is implemented"""
    cmd = ["dominion/rungame.py", "--validate_only", "--quiet", "--oldcards", "--card", card_name.lower()]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return False
    return True


##############################################################################
def main() -> None:
    """Main"""
    url = "https://wiki.dominionstrategy.com/api.php"
    params = {
        "action": "query",
        "generator": "categorymembers",
        "gcmtitle": "Category:Cards",
        "format": "json",
    }

    for result in get_html_data(url, params):
        for _, details in result["pages"].items():
            if ":" not in details["title"]:
                if not validate_card(details["title"]):
                    print(details["title"])


##############################################################################
if __name__ == "__main__":
    main()
