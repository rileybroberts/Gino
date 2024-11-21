import deck
import deadwood
from itertools import combinations
import time
import json
import ast

#TODO: Check running time of algorithm WITHOUT including number of cards left.
#      If it is good enough think about implementing number of cards left

class TDQL:

    qPath = 'qtable.txt'

    numCards = 11

    #Hyperparameters
    alpha = 0.10
    gamma = 0.95
    N_E = 11 #11 next possible actions, seems right, may be high due to scale

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

    def train(self, numEpisodes):
        converged = False
        currIterations = 0

        while converged == False and currIterations < numEpisodes:
            currIterations += 1
            converged = True

            #New Deck
            stock = deck.Deck()

            #Deal numCards cards
            state = []
            for c in range(self.numCards):
                state.append(stock.dealCard())

            reward = self.reward(state)

            print(f"state: {state}")
            print(f"reward: {reward}")

            #Run through training until
            # while reward != 10 and self.stock.cardsLeft > 1:
            #     action = self.policy(state)

            #     nextState = state.remove[]          #Discards card according to action
            #     nextState.append(stock.dealCard())  #Deals new card
            #     nextState.sort()                    #Sorts hand so order doesn't matter

            #     #This next bit is the Q learning function broken down
            #     maxNextQ = max(self.Q.get((nextState, m)) for m in self.moves.get(nextState[0]))
            #     oldQ = self.Q[(state,action)]
            #     self.Q[(state, action)] += self.alpha * ( reward + self.gamma * float(maxNextQ) - oldQ)

            #     #Check if still converging
            #     if abs(self.Q[(state,action)] - oldQ) > 0.005:
            #         converged = False
            
            print(currIterations)
            if converged:
                print("Holy shit we did it its converged")

    def initQTable(self):
        startTime = time.time()
        self.stock = deck.Deck()
        iter = 0
        for hand in combinations(self.stock.possibleCards,len(self.actions)):
            #This is all info about the hand so it is unique to each state but crucial for rewards
            melds, dw, _ = deadwood.compute_deadwood(hand)
            state = hand

            iter += 1
            print(f"hand : {iter}")
            for action in self.actions:
                #Necessary to build mini reward function here as opposed to calling
                #Otherwise we would need deadwood dict, doubling size
                if len(dw) == 0:
                    self.Q[(state, action)] = (10, 0, len(melds), len(dw))
                else:
                    self.Q[(state, action)] = (len(melds)-4, 0, len(melds), len(dw))
                

        with open(self.qPath, 'w') as f:  
            for key, value in self.Q.items():  
                f.write('%s:%s\n' % (key, value))

        print(self.stock.possibleCards)
        print(len(self.actions))
        print(f"actions:{self.actions}")
        print(len(self.Q))
        print(time.time()-startTime)

    #Exploration / Exploitation Policy
    def policy(self, state):

        #For now I am implementing an exploration function
        #In the future perhaps combine with greedy epsilon
        #E.g. if num is met go with low value epsilon i.e. 0.1

        #Since N(s,a) will always take precidence over Q(s,a)
        #We can just check to find min N(s,a).
        #If all s,a > N_E we can then do argmax Q(s,a)

        min_n = self.N_E
        min_a = 0

        for m in self.actions:
            if self.Q.get((state,m))[1] < min_n:
                min_n = self.Q.get((state,m))[1]
                min_a = m

        #Only runs if N_E satisfied for all actions
        if min_n != self.N_E:
            return min_a

        #Get action with max Q value
        action_q_values = [(self.Q.get((state, m)), m) for m in self.actions]
        _, a = max(action_q_values, key=lambda x: x[0])

        return a
    
    def reward(self, state):
        #State is in form [list of cards]
        #We grab a Q dict with an arbitrary action so we can access numMelds & cardsLeft
        
        #Win state
        #This can be 0 or 1 since we have 11 cards but only 10 need to fit since 1 gets thrown away
        #Fun fact: 11 card gin is called GunYang in SoCal (Pronounced Goon-yong)
        if self.Q.get(state,0)[3] in (0,1):
            return 10
        
        #The less melds it has the worse its reward (-1,-4)
        return self.Q.get(state,0)[2] - 4
        
    def qvalue(self, state, action):
        return self.get((state,action))[0]
    
    #Reads current Q table in from file
    def readQTable(self):
        self.Q = {}
        with open(self.qPath, 'r') as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                try:
                    key_str, value_str = line.split(':', 1)  # Split only at the first colon
                    key = ast.literal_eval(key_str)
                    value = ast.literal_eval(value_str)
                    self.Q[key] = value
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing line {line_number}: {line}")
                    print(f"Exception: {e}")
    
t = TDQL()
t.initQTable()
t.train(2)

