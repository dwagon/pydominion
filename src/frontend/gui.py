#!/usr/bin/env python

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from PIL import Image, ImageTk
import requests

domurl = 'http://localhost:5000'


##############################################################################
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()
        self.createCardStacks()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()

    def createBigcard(self):
        self.bigcard = tk.Button(self)
        img = Image.open('images/_card_back.jpg')
        img = img.resize((296, 473), Image.ANTIALIAS)
        self.bigcard._img = ImageTk.PhotoImage(img)
        self.bigcard["image"] = self.bigcard._img
        self.bigcard.pack(side="left")

    def createCardStacks(self):
        self.createBigcard()
        self.basecardframe = tk.Frame(self)
        self.kdomcardframe = tk.Frame(self)
        cardpiles = domget('/deck/list')
        self.cardpiles = {}
        for card in cardpiles:
            carddetails = domget('/card/%s' % card)
            if carddetails['basecard']:
                self.cardpiles[card] = CardStack(card, carddetails, self.basecardframe, self.bigcard)
            else:
                self.cardpiles[card] = CardStack(card, carddetails, self.kdomcardframe, self.bigcard)
        self.basecardframe.pack(side="top")
        self.kdomcardframe.pack(side="top")


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
    return r.json()


##############################################################################
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

##############################################################################
if __name__ == "__main__":
    main()

# EOF
