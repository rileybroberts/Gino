import deck
import game_state as state

class GinGame:

    hands = [[],[]]
    stockPile = deck.Deck()
    gameState = state.GameState()

    def beginGame(self):
        self.gameState = state.GameState()
        #Deal players 10 cards each then player 2 an 11th card
        for c in range(10):
            for p in range(2):
                self.hands[p].append(self.stockPile.dealCard())
        self.hands[1].append(self.stockPile.dealCard())
