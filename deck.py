from collections import deque
import random

class Deck:
    cardStack = []
    possibleCards = []

    def __init__(self):
        self.newDeck()
        self.possibleCards = self.cardStack.copy()
        self.possibleCards.sort()

    #Creates a fresh deck of shuffled cards
    def newDeck(self):
        self.cardStack = []
        #Removing a suit (D) for scaling reasons
        for suit in ("S","H","C"):
            #No face cards for scaling reasons
            for value in ("2","3","4","5","6","7","8"):
                self.cardStack.append(value+ suit)

        return self.cardStack    

    def shuffleDeck(self):
        #Shuffles the fresh deck
        random.shuffle(self.cardStack)

    def newShuffled(self):
        self.newDeck()
        self.shuffleDeck()

        return self.cardStack
 
    #Deals the top card off the deck
    def dealCard(self):
        return self.cardStack.pop()
    
    def cardsLeft(self):
        return len(self.cardStack)