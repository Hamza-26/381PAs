from backup import *
from search_helper import *
from collections import Counter

class CallCounter:
    def __init__(self, obj):
        self.object = obj # the object being wrapped, for this assignment, it will be a Problem object
        self.counter = Counter() # the count dictionary for function calls
        
    def __getattr__(self, attr):
        self.counter[attr] += 1 # everytime function attr is called, increment the counter for it
        return getattr(self.object, attr) # then call the function 


"""
    Given a list of searchers and problems, prints the statistics report.
"""
def print_stat_report(searchers, problems, searcher_names=None):
    for i, searcher in enumerate(searchers):
        sname = searcher.__name__
        if searcher_names is not None:
            sname = searcher_names[i]
        print(sname)
        total_counts = Counter()
        for p in problems:
            prob   = CallCounter(p) # wrap the problem object in the counter
            soln   = searcher(prob) # run search algorithm
            counter = prob.counter;  # get the counter dict
            
            # get solution cost
            if soln is None:        
                counter.update(solndepth=0, solncost=0)
            else:
                counter.update(solndepth=soln.depth, solncost=soln.path_cost)
                
            # maintain total for the current search algorithm
            total_counts += counter
            print_counts_helper(counter, str(p)[:30])
        print_counts_helper(total_counts, 'TOTAL\n')
        print('----------------------------------------------------------------')
        
def print_counts_helper(counter, name):
    print('{:9,d} generated nodes |{:9,d} popped |{:5.0f} solution cost |{:8,d} solution depth | {}'.format(
          counter['result'], counter['is_goal'], counter['solncost'], counter['solndepth'], name))

if __name__ == "__main__":
    nxn_problem1 = NxNGridProblem(initial_state=(5, 5), goal_state=(10, 10), N=10)
    nxn_problem2 = NxNGridProblem(initial_state=(1, 1), goal_state=(5, 5), N=10)
    nxn_problem3 = NxNGridProblem(initial_state=(1, 1), goal_state=(10, 10), N=10)

    # get some statistics on generated nodes, popped nodes, solution
    searchers = [(lambda p: best_first_search(p, bfs_f)), (lambda p: best_first_search(p, ucs_f))]
    problems = [nxn_problem1, nxn_problem2, nxn_problem3]
    print_stat_report(searchers, problems, searcher_names=['BFS', 'UCS'])