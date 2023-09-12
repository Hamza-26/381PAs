import numpy as np
import copy

def tour_cost(state,adj_matrix):
    sum = 0
    for i in range(len(state)-1):
        sum += adj_matrix[state[i]][state[i+1]]
    return sum

def random_swap(state):
    idx1, idx2 = np.random.choice(len(state), size=2,replace=False)
    
    s = copy.deepcopy(state)
    tmp = s[idx1]
    s[idx1] = s[idx2]
    s[idx2] = tmp
    return s


def simulated_annealing( initial_state, adj_matrix, initial_T = 1000):
    
    T = initial_T
    curState = initial_state
    iters = 0
    while True:
        T *= .99
        if T < 1e-14:
            return curState, iters
        next = random_swap(curState)
        deltaE = tour_cost(curState,adj_matrix) - tour_cost(next,adj_matrix)
        if deltaE > 0:
            curState = next 
        elif deltaE <= 0:
            u = np.random.uniform()
            if u <= np.e ** (deltaE/T):
                curState = next
        
        iters+=1
