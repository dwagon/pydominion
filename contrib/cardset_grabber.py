#!/usr/bin/env python
""" Grab recommended sets of cards from wiki.dominionstrategy.com """
import argparse
import string
import sys
from typing import Optional

import requests
from bs4 import BeautifulSoup


##############################################################################
def get_html(url: str) -> str:
    """Get the HTML from the url"""
    req = requests.get(url)
    req.raise_for_status()
    return req.text


##############################################################################
def get_set_name(item) -> Optional[str]:
    """Get the name of the set"""
    for kid in item.descendants:
        if kid.name is None:
            if kid.startswith(" ") and kid.endswith(" "):
                return kid.text.strip()
    print(f"Couldn't find set name in {item}", file=sys.stderr)
    return None


##############################################################################
def get_card_name(item) -> Optional[str]:
    """Get the card name"""
    return item.text.strip()


##############################################################################
def save_set(name, cards, expansion):
    """Save the set"""
    fname = name.replace(" ", "_")
    fname = fname.replace("&", "_and_")
    fname = fname.replace("'", "")
    print(f"Saving {fname} from {expansion}", file=sys.stderr)
    with open(fname, "w", encoding="utf-8") as outfh:
        outfh.write(f"# {expansion}\n")
        for card in sorted(cards):
            card = card.strip()
            if not card:
                continue
            if card in ("images",):
                continue
            outfh.write(f"{card}\n")


##############################################################################
def parse_table(table, expansion):
    """Parse the table recommended sets of 10 section"""
    cards = []
    set_name = None
    for item in table.children:
        if not set_name and item.name == "tr":
            set_name = get_set_name(item)
    if not set_name:
        return
    for item in table.find_all("a"):
        cards.append(get_card_name(item))
    if set_name[0] in string.ascii_uppercase:
        save_set(set_name, cards, expansion)


##############################################################################
def get_expansion():
    """Process args to get expansion"""
    parser = argparse.ArgumentParser(description="Get Recommended Sets")
    parser.add_argument("expansion")
    args = parser.parse_args()
    return args.expansion


##############################################################################
def main():
    """Main"""
    expansion = get_expansion()
    url = f"http://wiki.dominionstrategy.com/index.php/{expansion}"
    try:
        html = get_html(url)
    except requests.exceptions.HTTPError as exc:
        print(f"Couldn't get {url}\n\t{exc}")
        return

    soup = BeautifulSoup(html, "html.parser")
    for h2 in soup.find_all("h2"):
        if "Recommended sets " in h2.text:
            for item in h2.next_elements:
                if item.name == "table":
                    parse_table(item, expansion)
                if item.name == "h2":
                    break


##############################################################################
if __name__ == "__main__":
    main()

# EOF
