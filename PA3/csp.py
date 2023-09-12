import copy
import matplotlib.pyplot as plt
import seaborn as sns
def ac3(csp, arcs_queue=None, current_domains=None, assignment=None):
    if arcs_queue == None:
        arcs_queue = set([])
        for x in csp.adjacency:
            for y in csp.adjacency[x] :
                arcs_queue.add((x,y))
    arcs_queue = set(arcs_queue)
    if current_domains == None: current_domains = copy.deepcopy(csp.domains)
    updated_domains = current_domains
    
    while len(arcs_queue)!=0:
        (x1,x2) = arcs_queue.pop()
        if revise(csp,updated_domains,x1,x2):
            if len(updated_domains[x1])==0: return False,updated_domains
            for xk in  csp.adjacency[x1]:
                if xk != x2 and assignment!=None and  not xk in assignment: arcs_queue.add((xk,x1))

    return True,updated_domains


def revise(csp,domain, x1, x2):
    revised = False
    i =0
    while i < len(domain[x1]):
        x = list(domain[x1])[i]
        e = False
        for y in domain[x2]:
            if csp.constraint_consistent(x1,x,x2,y):
                e = True
                break
        if not e:
            domain[x1].remove(x)
            revised = True
            i-=1
        i+=1
        
    return revised




def backtracking(csp):
    return backtracking_helper(csp,{},current_domains=csp.domains)
        
def backtracking_helper(csp, assignment ={}, current_domains=None):
    if len(assignment) == len(csp.variables): return assignment
    var = select_unassigned_variable(assignment,csp,current_domains)
    for valu in current_domains[var]:
        
        if True:
            assignment[var] = valu
            copiedD = copy.deepcopy(current_domains)
            copiedD[var] = [valu]
            possible,dom = ac3(csp,arcs_queue=None,current_domains=copiedD,assignment=assignment)
            if possible :
                
                result = backtracking_helper(csp,copy.deepcopy(assignment),dom)
                if result != None : return result
            assignment.pop(var)
    return
def select_unassigned_variable(assignment, csp,domains):
    unassigned = [var for var in csp.variables if var not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))
   
   
   
   
   
         
         
class SudokuCSP:
    def __init__(self,partial_assignment={}):
        self.variables = [(r+1,c+1) for r in range(9) for c in range(9)]
        self.domains = {}
        for var in self.variables:
            if var in partial_assignment:
                self.domains[var] = [partial_assignment[var]]
            else: self.domains[var] = [i+1 for i in range(9)]
        
        self.adjacency = dict()
        
        for var in self.variables:
            self.adjacency[(var)] = set([])
            for i in range(1,10):
                if i != var[0]: self.adjacency[var].add((i,var[1]))
                if i != var[1]: self.adjacency[var].add((var[0],i))
            self.adjacency[var] =self.adjacency[var].union(set([(r,c) for r in range(-3*(-var[0]//3)-2,-3*(-var[0]//3)+1)  for c in range(-3*(-var[1]//3)-2,-3*(-var[1]//3)+1) if (r,c)!= var])) 
            # self.adjacency = list(set(self.adjacency))
            
    def constraint_consistent(self,var1,val1,var2,val2):
        return (not var2 in self.adjacency[var1]) or val1!= val2
              
    def check_partial_assignment(self,assignment):
        for v1 in assignment:
            for v2 in assignment:
            
                if not self.constraint_consistent(v1,assignment[v1],v2,assignment[v2]): return False
        return True
    
    def is_goal(self,assignment):
        return assignment!= None and (len(self.variables)==len(assignment) and self.check_partial_assignment(assignment))
    
      
                       
              
        

def visualize_sudoku_solution(assignment_solution, file_name):
    sudArray = [[0 for _ in range(9)] for _ in range(9)]
    for var in assignment_solution:
        sudArray[var[0]-1][var[1]-1] = assignment_solution[var]
        
    plt.figure(figsize=(9, 9))
    hm = sns.heatmap(data=sudArray,annot=True,linewidths=1.5,linecolor='k',cbar=False)
    hm.invert_yaxis()
    
    
    plt.savefig(file_name)
    plt.close()