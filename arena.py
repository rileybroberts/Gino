import TDQL
import deck
import random

'''
Todo List:
-Implement a random actor function that takes in number of episodes and outputs total rewards 
    (maybe win rate? Use if reward == 10)
-Implement a function that does the same but using the TDQL alg / Q table
-Implment a function that calls both of them and then gives the results
'''

class Arena:
    gino = TDQL.TDQL()

    def __init__(self) -> None:
        self.gino = TDQL.TDQL()
        self.gino.readQTable()

    def randomActor(self, numEpisodes):
        totalRewards = 0
        totalWins = float(0)

        for episode in range(numEpisodes):
            stock = deck.Deck()
            stock.shuffleDeck()

            hand = []
            for x in range(11):
                hand.append(stock.dealCard())
            hand.sort()

            reward = self.gino.reward(hand)

            while reward!= 10 and stock.cardsLeft() > 1:
                reward = self.gino.reward(hand)
                totalRewards += reward
                
                if (reward == 10):
                    totalWins += 1
                    break

                del hand[random.randint(0,10)]
                hand.append(stock.dealCard())
                hand.sort()
        
        winRate = totalWins / numEpisodes
        return totalRewards, winRate
    
    def ginoActor(self, numEpisodes):

        totalRewards = 0
        totalWins = float(0)

        for episode in range(numEpisodes):
            stock = deck.Deck()
            stock.shuffleDeck()

            hand = []
            for x in range(11):
                hand.append(stock.dealCard())
            hand.sort()

            reward = self.gino.reward(hand)

            while reward!= 10 and stock.cardsLeft() > 1:
                reward = self.gino.reward(hand)
                totalRewards += reward
                
                if (reward == 10):
                    totalWins += 1
                    break

                del hand[self.gino.policy(hand)]
                hand.append(stock.dealCard())
                hand.sort()
        
        winRate = totalWins / numEpisodes
        return totalRewards, winRate
    
    def battle(self, numEpisodes):
        ginoRewards, ginoWinrate = self.ginoActor(numEpisodes)
        randoRewards, randoWinrate = self.randomActor(numEpisodes)

        print(f"Gino --------- Total Rewards: {ginoRewards}")
        print(f"Gino -------------- Win Rate: {ginoWinrate}")
        print(f"Random Actor - Total Rewards: {randoRewards}")
        print(f"Random Actor ------ Win Rate: {randoWinrate}")

arena = Arena()
arena.battle(100000)