from collections import deque
import random

class Deck():
    cardStack = []

    def __init__(self):
        self.freshDeck()

    #Creates a fresh deck of shuffled cards
    def freshDeck(self):
        cardStack = []
        for suit in ("S","D","C","H"):
            for value in range(14, 1, -1):
                self.cardStack.append((value, suit))

        #Shuffles the fresh deck
        random.shuffle(self.cardStack)
 
    #Deals the top card off the deck
    def dealCard(self):
        return self.cardStack.pop()