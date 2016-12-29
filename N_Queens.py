# The eight queens puzzle is the problem of placing eight chess queens 
# on an 8×8 chessboard so that no two queens threaten each other.

# The main classes are defined in CSPmain.py
# In practice you only need Graph() and Solver()
from CSPmain import *

N = 12 #size of chessboard
# The constraint problem is modelled as a discrete binary graph, i.e. variables are represented in nodes together with
# their allowed values (i.e. their domains). The constraints are modelled as the edges of the graph, given as Boolean functions.
# Nodes can be addressed via keys, which can be any immutable data type.
P = Graph() # creates an empty problem

#The domain is an N x N matrix, starting to count with 0
domain = []
for row in range(N):
	for col in range(N):
		domain.append((row,col))

# The nodes (here queens) have to be added first. Their key is just an ID number
# new_node( <key>, <domain> )
for queen_id in range(N):
	P.new_node(queen_id,domain)	
queens = list(range(N)) #list of all queen_id's
# alternatively, a node could be created first and then added to the problem afterwards:
# mynode = Node(queen_id,domain)
# P.add_node(mynode)	


# Now the constraints have to be added
# here: no two queens may be on the same row, column, or diagonal
# the constraint is defined as a set of participating nodes (defined via their key or python reference) and 
# a Boolean function, which should evaluate to true for these nodes
def diff_row(x,y): return x[0] != y[0]
def diff_col(x,y): return x[1] != y[1]
def diff_diagA(x,y): return x[0]-x[1] != y[0]-y[1]
def diff_diagB(x,y): return x[0]+x[1] != y[0]+y[1]

# new_constraint( <constraint condition>, <list of nodes> , <optional argument> )
P.new_constraint(diff_row,queens,"mutual")
P.new_constraint(diff_col,queens,"mutual")
P.new_constraint(diff_diagA,queens,"mutual")
P.new_constraint(diff_diagB,queens,"mutual")
# "mutual" automatically applies the constraint to all binary combinations of nodes
# without "mutual" the function will be interpreted as a single n-dimensional constraint
# alternatives are:
# myconstraint = Constraint( <function>, [ <node key1> , ....])
# P.add_constraint(myconstraint)


# if for some reason the value of a node is known in advance, the domain 
# of the corresponding node simply should be set to this value
# P.set_value(<mynode>,<value>)


#Initialize solver, find solution and display it
X = Solver(P) #Solver has to be initialized with _fully_ defined problem graph

# The main search routine:
# Uses backtracking + AC3 pruning at each step to reduce domain size
# Always selects an open node with smallest domain size
X.search_solution()

X.display_solution()

