import deck
import deadwood

class TDQL:

    #Hyperparameters
    alpha = 0.10
    gamma = 0.95
    N_E = 11 #11 next possible actions, seems right, may be high due to scale

    #epsilon not currently in use but may be implemented later
    epsilon = 0.1

    #Q is a dict in form (state, action) : (qValue, timesExplored)
    Q = {}
    
    moves = [0,1,2,3,4,5,6,7,8,9,10]

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

        for m in self.moves:
            if self.Q.get((state,m))[1] < min_n:
                min_n = self.Q.get((state,m))[1]
                min_a = m

        #Only runs if N_E satisfied for all actions
        if min_n != self.N_E:
            return min_a

        #Get action with max Q value
        action_q_values = [(self.Q.get((state, m)), m) for m in self.moves]
        _, a = max(action_q_values, key=lambda x: x[0])

        return a
    
t = TDQL()
t.Q = {
    ("s1", 0) : (4, 12),
    ("s1", 1) : (3, 12),
    ("s2", 1) : (1, 1)
}
print(t.policy(("s1")))
    


