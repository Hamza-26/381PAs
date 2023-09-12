"""
Suppose you have an 𝑁×𝑁 grid. Suppose that we refer to each grid location using (row,column) coordinates. 
The agent starts at some grid location. The agent has four actions available: move left, right, up, or down. 
The grid is surrounded by walls, so if the agent moves outside of the 𝑁×𝑁 grids, it stays in place. 
The goal is for the agent to get to grid location (𝐺𝑟𝑜𝑤,𝐺𝑐𝑜𝑙). Answer the following in terms of 𝑁 when appropriate.]

For state formulation, we will use state = (row, column). Goal condition is that state == (G_row, G_col)
We'll use that row and col range from [1, 2, ..., N]
Assume all action costs are just 1


Need to define following functions:
1. constructor
2. actions
3. result
4. action_cost
5. is_goal 

state = (row, column)
"""

class NxNGridProblem:
    def __init__(self, initial_state, goal_state, N):
        self.initial_state = initial_state
        self.goal_state = goal_state   
        self.N = N
        
    def actions(self, state):
        row, col = state
        
        available_actions = ['up', 'down', 'left', 'right']
            
        return available_actions
        
    def result(self, state, action):
        row, col = state
        
        if action == 'up' and row == self.N:
            new_state = (row, col)
            return new_state
        elif action == 'down' and row == 1:
            new_state = (row, col)
            return new_state
        elif action == 'right' and col == self.N:
            new_state = (row, col)
            return new_state
        elif action == 'left' and col == 1:
            new_state = (row, col)
            return new_state
        
        if action == 'up':
            new_state = (row+1, col)
        elif action == 'down':
            new_state = (row-1, col)
        elif action == 'left':
            new_state = (row, col-1)
        elif action == 'right':
            new_state = (row, col+1)
            
        return new_state    
        
    def is_goal(self, state):
        row, col = state
        goal_row, gol_col = self.goal_state
        
        goal_condition = (row == goal_row) and (col == goal_col)
        
        return goal_condition
        
    def action_cost(self, state1, action, state2):
        return 1