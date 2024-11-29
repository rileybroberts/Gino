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

    def randomActor(numEpisodes):
        totalRewards = 0
        totalWins = float(0)

        for episode in numEpisodes:
            stock = deck.Deck()
            stock.shuffleDeck()

            hand = []
            for x in range(11):
                hand.append(stock.dealCard)
            hand.sort()

            reward = TDQL.reward(hand)

            while reward!= 10 and stock.cardsLeft() > 1:
                reward = TDQL.reward(hand)
                totalRewards += reward
                
                if (reward == 10):
                    totalWins += 1
                    break

                del hand[random.randint(0,11)]
                hand.append(stock.dealCard())
                hand.sort()
        
        winRate = totalWins / numEpisodes
        return totalRewards, winRate
    
    def gino(numEpisodes):
        totalRewards = 0
        totalWins = float(0)

        for episode in numEpisodes:
            stock = deck.Deck()
            stock.shuffleDeck()

            hand = []
            for x in range(11):
                hand.append(stock.dealCard)
            hand.sort()

            reward = TDQL.reward(hand)

            while reward!= 10 and stock.cardsLeft() > 1:
                reward = TDQL.reward(hand)
                totalRewards += reward
                
                if (reward == 10):
                    totalWins += 1
                    break

                del hand[TDQL.policy(hand)]
                hand.append(stock.dealCard())
                hand.sort()
        
        winRate = totalWins / numEpisodes
        return totalRewards, winRate