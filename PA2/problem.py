class ConstrainedRouteProblem:
    def __init__(self,initial_agent_loc,goal_loc,map_edges,map_coords,must_visit):
        self.initial_agent_loc = initial_agent_loc
        self.goal_loc = goal_loc
        self.map_edges = map_edges
        self.map_coords = map_coords
        self.must_visit = must_visit
        self.initial_state = tuple([initial_agent_loc]+[False for x in range(len(must_visit)+2)])
    def actions(self,state):
        l = []
        for edge in self.map_edges:
            if state[0] == edge[0]:
                l.append(edge[1])
            elif state[0] == edge[1]:
                l.append(edge[0])
        return l
    def result(self,state,action):
        booleans = [state[1],state[2]]
        for i,l in enumerate(self.must_visit):
            if l==action:
                booleans.append(True)
            else:
                booleans.append(state[i+3])
        if action ==self.goal_loc:
            if not state[1]:
                booleans[0] = True
            else: booleans[1] = True

        return tuple([action]+booleans)
    
    def action_cost(self,state1,action,state2):
        for edge in self.map_edges:
            if (state1[0],state2[0]) == edge or (state2[0],state1[0]) == edge :
                return self.map_edges[edge]
    
    def is_goal(self,state):
        if (not state[0] == self.goal_loc): return False
        if (not state[1] )or state[2]: return False
        for i in range(3,len(state)):
            if not state[i]: return False
        return True
    
    def h(self,node):
        return (((self.map_coords[node.state[0]][0])-(self.map_coords[self.goal_loc][0]))**2 + ((self.map_coords[node.state[0]][1])-(self.map_coords[self.goal_loc][1]))**2)**0.5
    



class GridProblemWithMonsters:
    def __init__(self,initial_agent_loc,N,monster_coords,food_coords):
        self.initial_agent_loc = initial_agent_loc
        self.N = N
        self.monster_coords = monster_coords
        self.food_coords = food_coords
        self.initial_state = tuple(list(initial_agent_loc)+[0]+[False for f in food_coords])
    
    def actions(self,state):
        acts = []
        U = state[0] < self.N
        D = state[0] > 1
        R = state[1] < self.N
        L = state[1] > 1
        S = True
        for m in self.monster_coords:
            if (state[2]==1 or state[2]==3): futureMonsterLoc = (m[0],m[1])
            elif(state[2]==0): futureMonsterLoc = (m[0],m[1]-1)
            else: futureMonsterLoc = (m[0],m[1]+1)
            if U and (((state[0]+1,state[1]) == futureMonsterLoc)) :
                U = False
            if D and (((state[0]-1,state[1]) == futureMonsterLoc) ):
                D = False
            if R and (((state[0],state[1]+1) == futureMonsterLoc)):
                R = False
            if L and (((state[0],state[1]-1) == futureMonsterLoc)):
                L = False
            if S and ((state[0],state[1]) == futureMonsterLoc):
                S = False

        if U: acts.append('up')
        if D: acts.append('down')
        if R: acts.append('right')
        if L: acts.append('left')
        if S: acts.append('stay')
        return acts
    
    def result(self,state,action):
        rState = list(state[3:])
        if action == 'up':
            futurePos = (state[0]+1,state[1])
        elif action == 'down':
            futurePos = (state[0]-1,state[1])
        elif action == 'right':
            futurePos = (state[0],state[1]+1)
        elif action == 'left':
            futurePos = (state[0],state[1]-1)
        elif action == 'stay':
            futurePos = (state[0],state[1])

        for i,fr in enumerate(self.food_coords):
            if fr==futurePos:
                rState[i] = True
                break
        
        return futurePos + tuple([(state[2]+1)%4])+ tuple(rState)
    
    def action_cost(self,state1,action,state2):
        return 1
    
    def is_goal(self,state):
        for k in state[3:]:
            if not k: return False
        return True
    
    def h(self,node):
        y = node.state
        if self.is_goal(y): return 0
        
        manhantan = [(abs(x[0]-y[0])+abs(x[1]-y[1])) for i,x in enumerate(self.food_coords) if not y[i+3]]
        return min(manhantan)



