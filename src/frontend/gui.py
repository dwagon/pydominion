#!/usr/bin/env python

import sys
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from PIL import Image, ImageTk
import requests

domurl = 'http://localhost:5000'
try:
    plrnum = int(sys.argv[1])
except:
    plrnum = 0


##############################################################################
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.cardcache = {}
        self["borderwidth"] = 3
        self["relief"] = tk.GROOVE
        self["bg"] = "blue"
        self.pack()
        self.getPlayers()
        self.createWidgets(self)
        self.createBigcard(self)
        self.createCardStacks(self)
        self.createActionBar(self)
        self.createHand(self)
        self.createMessages(self)
        self.update_message()
        self.get_inputs()

    def get_inputs(self):
        inp = domget('/player/%s/inputs' % self.players[plrnum])
        print("inp=%s" % inp)
        self.after(500, self.get_inputs)

    def update_message(self):
        msg = domget('/player/%s/messages' % self.players[plrnum])
        self.messagebox.insert(tk.END, msg)
        self.after(500, self.update_message)

    def createMessages(self, master):
        self.messagebox = tk.Listbox(master, height=5)
        self.messagebox.pack()

    def getPlayers(self):
        self.players = domget('/player/list')
        print("players=%s" % self.players)

    def getCard(self, cardname):
        if cardname not in self.cardcache:
            self.cardcache[cardname] = domget('/card/%s' % cardname)
        return self.cardcache[cardname]

    def createActionBar(self, master):
        self.etButton = tk.Button(master, text='End Turn', command=self.action_endturn)
        self.etButton.pack()

    def action_endturn(self):
        self.players = domget('/endturn')

    def createWidgets(self, master):
        self.quitButton = tk.Button(master, text='Quit', command=self.quit)
        self.quitButton.pack()

    def createHand(self, master):
        self.handframe = tk.Frame(self, bg="orange")
        hand = domget('/player/%s/hand' % self.players[plrnum])
        for card in hand:
            carddetails = self.getCard(card)
            self.cardpiles[card] = CardStack(card, carddetails, self.handframe, self.bigcard)
        self.handframe.pack(side="top")

    def createBigcard(self, master):
        self.bigcard = tk.Button(master)
        img = Image.open('images/_card_back.jpg')
        img = img.resize((296, 473), Image.ANTIALIAS)
        self.bigcard._img = ImageTk.PhotoImage(img)
        self.bigcard["image"] = self.bigcard._img
        self.bigcard.pack(side="left")

    def createCardStacks(self, frame):
        self.cardstacks = tk.Frame(frame)
        self.cardstacks["bg"] = "red"
        self.basecardframe = tk.Frame(self.cardstacks)
        self.kdomcardframe = tk.Frame(self.cardstacks)
        cardpiles = domget('/deck/list')
        self.cardpiles = {}
        for card in cardpiles:
            carddetails = self.getCard(card)
            if not carddetails['purchasable']:
                continue
            if carddetails['basecard']:
                self.cardpiles[card] = CardStack(card, carddetails, self.basecardframe, self.bigcard)
            else:
                self.cardpiles[card] = CardStack(card, carddetails, self.kdomcardframe, self.bigcard)
        self.basecardframe.pack(side="top")
        self.kdomcardframe.pack(side="top")
        self.cardstacks.pack(side="top")


##############################################################################
class CardStack(tk.Frame):
    def __init__(self, card, details={}, master=None, bigcard=None):
        super().__init__(master)
        self.card = card
        self.details = details
        self.bigcard = bigcard
        self.button = tk.Button(master)
        self.button["text"] = card
        if details['image']:
            # Most images are 296, 473
            img = Image.open(details['image'])
            bigimage = img.resize((296, 473), Image.ANTIALIAS)
            self.bigimage = ImageTk.PhotoImage(bigimage)
            image = img.resize((74, 118), Image.ANTIALIAS)
            self.button._img = ImageTk.PhotoImage(image)
            self.button["image"] = self.button._img
            self.button.bind("<Enter>", self.on_enter)
            self.button.bind("<Leave>", self.on_leave)
        self.button.pack(side=tk.LEFT)

    def on_enter(self, event):
        self.bigcard.configure(image=self.bigimage)

    def on_leave(self, event):
        pass


##############################################################################
def domget(url):
    full_url = '%s%s' % (domurl, url)
    r = requests.get(full_url)
    if r.status_code != 200:
        sys.stderr.write("Got a %s from %s\n" % (r.status_code, full_url))
        sys.exit(1)
    return r.json()


##############################################################################
def main():
    root = tk.Tk()
    guiapp = Application(master=root)
    guiapp.mainloop()


##############################################################################
if __name__ == "__main__":
    main()

# EOF
