#!/usr/bin/env python
"""Grab recommended sets of cards from wiki.dominionstrategy.com"""
import argparse
import string
import time

import httpx
import bs4


##############################################################################
def get_html(url: str) -> str:
    """Get the HTML from the url"""
    req = httpx.get(url, follow_redirects=True)
    req.raise_for_status()
    return req.text


##############################################################################
def get_set_name(item: bs4.PageElement) -> str:
    """Get the name of the set from
        <tr>
        <th colspan="15" style="position:relative">Victory Dance <span class="mw-customtoggle-Victory_Dance" style="position:absolute;
    right:2px;">
        [<a href="#¬"><span>images</span></a>]</span>
        </th>
        </tr>"""
    try:
        return str(item.th.contents[0].strip())
    except:
        return ""


##############################################################################
def save_set(name: str, cards: list[str], expansion: str) -> None:
    """Save the set"""
    fname = name.replace(" ", "_")
    fname = fname.replace("&", "_and_")
    fname = fname.replace("'", "")
    with open(fname, "w", encoding="utf-8") as outfh:
        outfh.write(f"# {expansion} {time.ctime()}\n")
        for card in sorted(cards):
            card = card.strip()
            if not card:
                continue
            if card in ("images",):
                continue
            outfh.write(f"{card}\n")


##############################################################################
def parse_table(table: bs4.PageElement, expansion: str) -> None:
    """Parse the table recommended sets of 10 section"""
    cards = []
    set_name = None
    for item in table.children:
        if not set_name and item.name == "tr":
            set_name = get_set_name(item)
    if not set_name:
        print("No set name found")
        return
    for item in table.find_all("a"):
        if card_name := item.string:
            cards.append(card_name.strip())
    if set_name[0] in string.ascii_uppercase:
        save_set(set_name, cards, expansion)


##############################################################################
def get_expansion() -> str:
    """Process args to get expansion"""
    parser = argparse.ArgumentParser(description="Get Recommended Sets")
    parser.add_argument("expansion")
    args = parser.parse_args()
    return str(args.expansion)


##############################################################################
def main() -> None:
    """Main"""
    expansion = get_expansion()
    print(f"Scanning {expansion}")
    url = f"https://wiki.dominionstrategy.com/index.php/Recommended_Kingdoms/{expansion}"
    try:
        html = get_html(url)
    except httpx.HTTPError as exc:
        print(f"Couldn't get {url}\n\t{exc}")
        return

    soup = bs4.BeautifulSoup(html, "html.parser")
    for h2 in soup.find_all("h2"):
        for item in h2.next_elements:
            if item.name == "table":
                parse_table(item.tbody, expansion)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
