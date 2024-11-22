import deck
import deadwood
from itertools import combinations
import time
import ast
import random
from random import randrange

#TODO: Check running time of algorithm WITHOUT including number of cards left.
#      If it is good enough think about implementing number of cards left

class TDQL:

    qPath = 'qtable.txt'

    numCards = 3

    #Hyperparameters
    alpha = 0.10
    gamma = 0.95
    N_E = 11 #11 next possible actions, seems right, maybe high maybe way low

    #TODO: Implement total rewards testing once trained
    totalRewardsQL = 0
    totalRewardsRandom = 0

    #epsilon not currently in use but may be implemented later
    epsilon = 0.1

    #Q is a dict in form (state, action) : (qValue, timesExplored, numMelds, cardsLeft)
    #State is ([sorted card list])
    Q = {}
    actions = []

    def __init__(self):
        #Initiates action array based on numCards
        for i in range(self.numCards):
            self.actions.append(i)
        
    #TODO: For some reason it is visiting the same state during each trial
    def train(self, numEpisodes):
        start = time.time()
        converged = False
        currIterations = 0

        while converged == False and currIterations < numEpisodes:
            currIterations += 1
            # converged = True
            converged = False #TODO: Fix Convergence Check

            #New Deck
            stock = deck.Deck()
            stock.shuffleDeck()

            #Deal numCards cards
            state = []
            for c in range(self.numCards):
                state.append(stock.dealCard())

            state.sort()

            reward = self.reward(state)

            while reward != 10 and stock.cardsLeft() > 1:
                reward = self.reward(state)
                if (reward == 10):
                    break

                action = self.policy(state)
                state = list(state)

                nextState = state.copy()
                del nextState[action]               #Discards card according to action
                nextState.append(stock.dealCard())  #Deals new card 
                nextState.sort()                    #Sorts hand so order doesn't matter
                nextState = tuple(nextState)
                state = tuple(state)

                #This next bit is the Q learning function broken down
                maxNextQ = max(self.Q.get((nextState, a)) for a in self.actions)
                maxNextQ = maxNextQ[0]
                oldTuple = self.Q[(state,action)]
                self.Q[(state, action)] = (oldTuple[0] + self.alpha * ( reward + self.gamma * float(maxNextQ) - oldTuple[0]),  oldTuple[1] + 1, oldTuple[2], oldTuple[3])

                #Check if still converging
                if abs(self.Q[(state,action)][0] - oldTuple[0]) > 0.005:
                    converged = False

                state = nextState
            
            if converged:
                print(f"Holy shit we did it its converged. It took {currIterations} iterations")
        end = time.time()
        print(f"training took {end - start} seconds")

    def initQTable(self):
        start = time.time()
        self.stock = deck.Deck()
        for hand in combinations(self.stock.possibleCards,len(self.actions)):
            #This is all info about the hand so it is unique to each state but crucial for rewards
            melds, dw, _ = deadwood.compute_deadwood(hand)
            state = hand
            for action in self.actions:
                #Necessary to build mini reward function here as opposed to calling
                #Otherwise we would need deadwood dict, doubling size
                if len(dw) == 0:
                    self.Q[(state, action)] = (10, 0, len(melds), len(dw))
                else:
                    self.Q[(state, action)] = (len(melds)-4, 0, len(melds), len(dw))

        end = time.time()
        print(f"Qinit took {end - start} seconds")

    #Exploration / Exploitation Policy
    def policy(self, state):

        #For now I am implementing an exploration function
        #In the future perhaps combine with greedy epsilon
        #E.g. if num is met go with low value epsilon i.e. 0.1

        #Since N(s,a) will always take precidence over Q(s,a)
        #We can just check to find min N(s,a).
        #If all s,a > N_E we can then do argmax Q(s,a)

        minNum = self.N_E
        minAction = 0
        state = tuple(state)

        for m in self.actions:
            if self.Q.get((state,m))[1] < minNum:
                minNum = self.Q.get((state,m))[1]
                minAction = m

        #If minNum isn't what we set it to that means something is below N_E and we do that action
        if minNum != self.N_E:
            return minAction
        
        #Chance for Greedy Epsilon to choose random action incase we are stuck in local minima
        if (random.random() < self.epsilon):
            return randrange(self.numCards)

        #Otherwise get action with max Q value
        action_q_values = [(self.Q.get((state, m)), m) for m in self.actions]
        _, a = max(action_q_values, key=lambda x: x[0])

        return a
    
    def reward(self, state):
        #State is in form [list of cards]
        #We grab a Q dict with an arbitrary action so we can access numMelds & cardsLeft
        
        #Win state
        #This can be 0 or 1 since we have 11 cards but only 10 need to fit since 1 gets thrown away
        #Fun fact: 11 card gin is called GunYang in SoCal (Pronounced Goon-yong)
        state = tuple(state)
        if self.Q.get((state,0))[3] in (0,1):
            return 10
        
        #The less melds it has the worse its reward (-1,-4)
        return self.Q.get((state,0))[2] - 4
        
    def qvalue(self, state, action):
        state = tuple(state)
        return self.get((state,action))[0]
    
    #Reads current Q table in from file
    def readQTable(self):
        start = time.time()
        self.Q = {}
        with open(self.qPath, 'r') as f:
            for line_number, line in enumerate(f, 1):
                print(f"line: {line_number}")
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                try:
                    # Split the line at the first colon to separate key and value
                    key_str, value_str = line.split(':', 1)
                    key_str = key_str.strip()
                    value_str = value_str.strip()

                    # Evaluate the key and value strings
                    key = ast.literal_eval(key_str)
                    value = ast.literal_eval(value_str)

                    # Store the parsed data into the Q-table
                    self.Q[key] = value

                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing line {line_number}: {line}")
                    print(f"Exception: {e}")
        end = time.time()
        print(f"Q read took {end-start} seconds")
    
    def writeQTable(self):
        start = time.time()
        with open(self.qPath, 'w') as f:  
            for key, value in self.Q.items():  
                f.write('%s:%s\n' % (key, value))
        end = time.time()
        print(f"writing Q table took {end - start} seconds")

t = TDQL()
t.initQTable()
t.train(50000)
t.writeQTable()

