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

    numCards = 3

    #Hyperparameters
    alpha = 0.10
    gamma = 0.95
    N_E = 11 #11 next possible actions, seems right, may be high due to scale

    #epsilon not currently in use but may be implemented later
    epsilon = 0.1

    #Q is a dict in form (state, action) : (qValue, timesExplored)
    #State is ([sorted card list], numMelds, value)
    Q = {}
    actions = []

    stock = deck.Deck()

    def __init__(self):
        for i in range(self.numCards):
            self.actions.append(i)

    def initQTable(self):
        startTime = time.time()
        self.stock = deck.Deck()
        iter = 0
        for hand in combinations(self.stock.possibleCards,len(self.actions)):
            #This is all info about the hand so it is unique to each state but crucial for rewards
            melds, _, value = deadwood.compute_deadwood(hand)
            state = (hand, len(melds), value)

            iter += 1
            print(f"hand : {iter}")
            for action in self.actions:
                self.Q[(state, action)] = (self.reward(state), 0)

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
        #State is in form ([list of cards], numMelds, value)

        #Win state
        if state[2] == 0:
            return 10
        
        if state[1] == 3:
            return -1
        
        if state[1] == 2:
            return -2
        
        if state[1] == 1:
            return -3
        
        else:
            return -4
        
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

