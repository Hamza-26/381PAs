import problem

class Node:
    def __init__(self,state, parent_node=None,action_from_parent=None, path_cost=0):
        self.state = state
        self.parent_node = parent_node
        self.action_from_parent = action_from_parent
        self.path_cost = path_cost
        if (parent_node == None): self.depth = 0
        else: self.depth = parent_node.depth + 1

    def __lt__(self, other):
        return self.state < other.state
    




import heapq
class PriorityQueue:
    def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
 # add the items to the PQ
        for item in items:
            self.add(item)

    """
    Add item to PQ with priority-value given by call to priority_function
    """
    def add(self, item):
        pair = (self.priority_function(item), item)
        heapq.heappush(self.pqueue, pair)
    """
    pop and return item from PQ with min priority-value
    """
    def pop(self):
        return heapq.heappop(self.pqueue)[1]
    """
    gets number of items in PQ
    """
    def __len__(self):
        return len(self. pqueue)
    

def expand(problem,node):
    s = node.state
    for action in problem.actions(s):
        ss = problem.result(s,action)
        cost = node.path_cost + problem.action_cost(s,action,ss)
        yield Node(state=ss,parent_node= node,action_from_parent=action,path_cost=cost)

def get_path_actions(node):
    if node == None or node.parent_node == None:
        return []
    list_of_actions = []
    parent = node.parent_node
    while (parent != None):
        list_of_actions.append(node.action_from_parent)
        node = parent
        parent = node.parent_node
    return list_of_actions[::-1]

def get_path_states(node):
    if node == None: return []
    list_of_states = []
    while (node != None):
        list_of_states.append(node.state)
        node = node.parent_node
    return list_of_states[::-1]

def best_first_search(problem,f):
    node = Node(state = problem.initial_state)
    frontier = PriorityQueue(priority_function=f)
    frontier.add(node)
    reached = {problem.initial_state : node}
    while not frontier.__len__() == 0:
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        for child in expand(problem,node):
            s = child.state
            if (not s in reached) or (child.path_cost < reached[s].path_cost) :
                reached[s] = child
                frontier.add(child)
    return None


def best_first_search_treelike(problem,f):
    node = Node(state = problem.initial_state)
    frontier = PriorityQueue(priority_function=f)
    frontier.add(node)
    while not frontier.__len__() == 0:
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        for child in expand(problem,node):
            s = child.state
            frontier.add(child)
    return None 

def breadth_first_search(problem,treelike = False):
    if treelike:
        return best_first_search_treelike(problem, f = lambda x : x.depth)
    else: 
        return best_first_search(problem,f = lambda x: x.depth)

def depth_first_search(problem, treelike = False):
    if treelike:
        return best_first_search_treelike(problem, lambda x : -x.depth)
    else: 
        return best_first_search(problem,f = lambda x: -x.depth)
    
def uniform_cost_search(problem,treelike = False):
    if treelike:
        return best_first_search_treelike(problem,f = lambda x : x.path_cost)
    else: 
        return best_first_search(problem,f = lambda x: x.path_cost)
    
def greedy_search(problem,h,treelike = False):
    if treelike:
        return best_first_search_treelike(problem,h)
    else: 
        return best_first_search(problem,h)
    
def astar_search(problem, h, treelike = False):
    if treelike:
        return best_first_search_treelike(problem,f =  lambda n: n.path_cost + h(n))
    else: 
        return best_first_search(problem,f =  lambda n: n.path_cost + h(n))


import matplotlib.pyplot as plt
# import matplotlib.patches as patches
def visualize_route_problem_solution(problem,goal_node,file_name):
    xCords =[]
    yCords =[]
    colors = []
    print(problem.map_coords)
    for location,c in problem.map_coords.items():
        xCords.append(c[0])
        yCords.append(c[1])
        if location == problem.initial_agent_loc:
            colors.append('r')
        elif location in problem.must_visit:
            colors.append('b')
        elif location == problem.goal_loc:
            colors.append('g')
        else: 
            colors.append('k')
        
    plt.scatter(x = xCords,y=yCords,c=colors,marker='s')

    for edge in problem.map_edges:
        plt.arrow(problem.map_coords[edge[0]][0],
                  problem.map_coords[edge[0]][1],
                  problem.map_coords[edge[1]][0]-problem.map_coords[edge[0]][0],
                  problem.map_coords[edge[1]][1]-problem.map_coords[edge[0]][1],
                  head_width =0)
    statesToGoal = get_path_states(goal_node)
    for i,s in enumerate(statesToGoal):
        if i != len(statesToGoal) -1 :
            nextS = statesToGoal[i+1]
            plt.arrow(problem.map_coords[s[0]][0],
                    problem.map_coords[s[0]][1],
                    problem.map_coords[nextS[0]][0]-problem.map_coords[s[0]][0],
                    problem.map_coords[nextS[0]][1]-problem.map_coords[s[0]][1],
                    color = 'm',
                    head_width =0.1)
    plt.savefig(file_name)
    plt.close()
        

def visualize_grid_problem_solution(problem, goal_node, file_name):
    xMonsters = [x[1] for x in problem.monster_coords]
    yMonsters = [y[0] for y in problem.monster_coords]
    plt.scatter(x=xMonsters, y=yMonsters, c='k',marker='*',s=2500)
    xFood = [x[1] for x in problem.food_coords]
    yFood = [x[0] for x in problem.food_coords]
    plt.scatter(x=xFood,y=yFood,c='g',marker='h',s= 1000)
    plt.scatter(x=[problem.initial_agent_loc[1]],y=[problem.initial_agent_loc[0]],
                c='r',marker='^',s=1000)
    statesToGoal = get_path_states(goal_node)
    for i,s in enumerate(statesToGoal):
        if i != len(statesToGoal) -1 :
            nextS = statesToGoal[i+1]
            plt.arrow(s[1],s[0],
                    nextS[1]-s[1],
                    nextS[0]-s[0],
                    color = 'm',
                    head_width =0.1)

    plt.ylim([0.5, problem.N + 0.5])
    plt.xlim([0.5, problem.N + 0.5])
    plt.savefig(file_name)
    plt.close()























