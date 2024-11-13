class GameState():
    playerHand = []
    discardPile = []
    moveSequence = []
    cardsLeft = 31
    whosTurn = 2
    pointsInHand = 1000

    def encodeState(self):
        encoded = [
            self.playerHand,
            self.discardPile,
            self.moveSequence,
            self.cardsLeft,
            self.whosTurn,
            self.pointsInHand
        ]

        return encoded


