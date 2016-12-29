import copy


# A node is simply a key + domain (set of permissible values) for a variable
class Node:	
	def __init__(this, key0 = None, domain0 = None):
		this.key = key0 #used to address and find node	
		if domain0 == None:
			domain0 = {}
		this.domain = set(domain0) 
		
	def is_satisfiable(this):
		return len(this.domain) > 0

	def domain_size(this):
		return len(this.domain)
	


# A constraint is a Boolean function + list of references to participating nodes	
# Binary constraints are usually called 'arcs'
class Constraint:	
	def __init__(this, func0 = None, nodes0 = None):
		this.func = func0 #function of Boolean type
		if nodes0 == None:
			nodes0 = []
		this.nodes = nodes0 

	# overloaded: if no values are explicitly given, the first domain entries of participating nodes are used
	# returns true iff function evaluates to true	
	def is_satisfied(this,values = None):
		if values == None:
			values = []
			for nd in this.nodes:
				if len(nd.domain) == 0:
					return False
				elif len(nd.domain) > 1:
					print("warning: value of node not set")
				values.append(list(nd.domain)[0])					
		return this.func(*values)
		
	# finds second node of a binary constraint (i.e. arc)
	def arc_neighbour_node(this,first_node):
		tmp = this.nodes
		if tmp[0] == first_node:
			neighbour_node = tmp[1]
		else:
			neighbour_node = tmp[0]
		return neighbour_node
	
		

# A DomainGraph is a collection of nodes
# Maintains a look-up table of key->node	
# DomainGraph has a copy constructor, using a deep copy
# Nodes can be added via add_node or new_node. Former adds an already existing node to the graph, latter creates a new one first
# Also provides get_node(key) which returns node when key is given
class DomainGraph:
	def __init__(this, other = None):
		if other == None:
			this.nodes = [] # list of all nodes of this graph
			this.node_lt = None
			this.node_lt_flag = False
		else:
			this.nodes = copy.deepcopy(other.nodes)
			this.generate_node_lt()			

	# adds an already existing node
	def add_node(this,new_node):
		this.nodes.append(new_node)
		this.node_lt_flag = False
	
	# creates a new node and adds it to the graph	
	def new_node(this,key,domain):
		new_node = Node(key,domain)
		this.nodes.append(new_node)
		this.node_lt_flag = False
		return new_node

	# overloaded: 
	# returns reference of node, when arg is either key or reference
	def get_node(this, arg):
		if not this.node_lt_flag:
			this.generate_node_lt()
		if isinstance(arg,Node):
			return arg
		else:
			return this.node_lt[arg]
		
	def get_domain(this, key):
		return this.get_node(key).domain
	
	# re-defines the domain of a given node	
	def set_value(this, key, value0):
		this.get_node(key).domain =  {value0}

	def generate_node_lt(this):
		this.node_lt = {this.nodes[0].key : this.nodes[0]}
		for nd in this.nodes[1:]:
			this.node_lt.update({nd.key : nd})
		this.node_lt_flag = True
		
	# find a smallest open node, open node = node of domain size > 1
	def smallest_open_node(this, node_sublist = None):
		if node_sublist == None:
			node_sublist = this.nodes
		min_node = None
		min_size = None
		for nd in node_sublist:
			tmp = nd.domain_size()
			if tmp > 1 and (min_size == None or tmp < min_size):
				min_node = nd
				min_size = min_node.domain_size()
		return min_node

	# finds all open nodes out of a given list
	def select_open_nodes(this, node_sublist = None):
		open_list = []
		if node_sublist == None:
			node_sublist = this.nodes
		for nd in node_sublist:
			if nd.domain_size() > 1:
				open_list.append(nd)
		return open_list
				
					
					

# A Graph is a DomainGraph + list of constraints
# Maintains a look-up table of constraints, that maps: node --> Set of involved constraints
class Graph(DomainGraph):	 
	def  __init__(this):
		DomainGraph.__init__(this)	 
		this.constraints = [] #[list of all constraints]
		this.constraint_lt = {x:set() for x in this.nodes}  #dictionary: node -> [set of involved constraints]
		this.constraint_lt_flag = False

	# Generates look up table for node -> its constraints
	def generate_constraint_lt(this):
		this.constraint_lt = {x:set() for x in this.nodes}
		for con in this.constraints:
			for nd in con.nodes:
				this.constraint_lt[nd].add(con)
		this.constraint_lt_flag = True
		return		 


	# overloaded, possible calls:
	# only one function and participating nodes 
	# nodes can be given as reference or by their key
	# if opt == "mutual", the function is interpreted as binary function, regardless of number of nodes given
	# then all possible combinations out of the given list of nodes are added with this binary constraint
	def new_constraint(this, func, nodes0, opt = None):
		nodes = []
		for nd in nodes0:
			if not isinstance(nd,Node):
				nodes.append(this.get_node(nd))
			else:
				nodes.append(nd)
		if opt == "mutual":
			for nd1 in nodes:
				for nd2 in nodes:
					if nd1 != nd2:
						this._new_constraint(func,[nd1,nd2])
		else:
			this._new_constraint(func,nodes)

	# helper for new_constraint()
	def _new_constraint(this, func, nodes):
		new_constraint = Constraint(func,nodes)			
		this.constraints.append(new_constraint)			
		this.constraint_lt_flag = False

	def add_constraint(this,new_constraint):
		this.constraints.append(new_constraint)			
		this.constraint_lt_flag = False	


	def check_binary(this):
		for con in this.graph.constraints:
			if len(con.nodes) != 2:
				print("error: ac3 current only works on binary constraints")
				return False
		return True



# Must be initialized with reference to graph to be solved
class Solver:
	def __init__(this, graph_orig):
		this.graph_orig = graph_orig #original graph, will not be altered
		this.graph = copy.deepcopy(graph_orig) #working copy, regularly modified
		this.graph.generate_node_lt()
		this.graph.generate_constraint_lt()
		this.solution_flag = None
	
	# Applies all unary constraints and removes them from this.graph
	def apply_unary(this):
		new_constraints = []
		for con in this.graph.constraints:
			if len(con.nodes) == 1:
				new_domain = []
				for entry in con.nodes[0].domain:
					if con.func(entry):
						new_domain.append(entry)
				if len(new_domain) == 0:
					print("Unary constraint not satisfiable")
					return False
				con.nodes[0].domain = new_domain
			else:
				new_constraints.append(con)
		this.graph.constraints = new_constraints
		return True
					
	# reduces domains of nodes, by using Arc Consistency 3 algorithm
	# assumes binary constraints
	# constraints_sublist is optional, limiting the constraints to be checked to this list
	# Returns false iff one domain is reduced to zero
	def apply_AC3(this, constraints_sublist = None):
		if constraints_sublist == None:
			worklist = copy.copy(this.graph.constraints)
		else:
			worklist = copy.copy(constraints_sublist)		
		while len(worklist) > 0:
			arc = worklist.pop(0)
			nd1 = arc.nodes[0]
			nd2 = arc.nodes[1]
			if this.filter_domain_single_arc(nd1,arc,nd2):
				if len(nd1.domain) == 0:
					return False
				else:
					worklist.extend(this.graph.constraint_lt[nd1])				
		return True
	
	
	# Reduces domain of current_node, such that all its values are consistent with arc
	# is used in AC3 algorithm
	def filter_domain_single_arc(this, current_node, arc, neighbour_node):		
		new_domain = set()
		for x in current_node.domain:
			for y in neighbour_node.domain:
				if arc.is_satisfied([x,y]):
					new_domain.add(copy.copy(x))
					break
		if new_domain == current_node.domain:
			return False
		else:
			current_node.domain = new_domain
			return True
	
	# Reduces domain of current_node until it is consistent with all neighbours
	# Returns true iff domain was reduced	
	def filter_domain_all_arcs(this,current_node):		
		pruned = False
		for arc in this.graph.constraint_lt[current_node]:
			neighbour_node = arc.arc_neighbour_node(current_node)
			pruned = pruned and this.filter_domain_single_arc(current_node,arc,neighbour_node)
		return pruned
		
	# Reduces domain, such that it is consistent with all constraints involving a closed node (domain size == 1)		
	def filter_domain_known_arcs(this,current_node):		
		pruned = False
		for arc in this.graph.constraint_lt[current_node]:
			neighbour_node = arc.arc_neighbour_node(current_node)
			if len(neighbour_node.domain) == 1:
				pruned = pruned and this.filter_domain_single_arc(current_node,arc,neighbour_node)
		return pruned
		
	# Generates a sublist of all constraints, which have at least one open node
	# Used for AC3 and search routine
	def select_open_constraints(this):
		selected_constraints = []
		for con in this.graph.constraints:
			active = False
			for nd in con.nodes:
				if len(nd.domain) > 1:
					active = True
					break
			if active:
				selected_constraints.append(con)
		return selected_constraints
	
		
	# Main search routine
	# Uses backtracking + AC3 pruning at each step to reduce domain size
	# Always proceeds with an open node with smallest domain size
	# Algorithm is recursive, helper function is _search_solution()		
	def search_solution(this):
		if this.apply_AC3():
			print("Looking for a solution via back tracking...")
			this.solution_flag = this._search_solution(this.graph.nodes)
			print("...done")
		else:
			print("Constraints are not arc consistent")
			this.solution_flag = False
		return this.solution_flag

	# Recursive search using backtracking
	# passes lists of open_nodes0, such that they do not have to be repeatedly double checked
	def _search_solution(this, open_nodes0):		
		# reduce set of open nodes		
		open_nodes = copy.copy(open_nodes0)		
		open_nodes = this.graph.select_open_nodes(open_nodes)
		
		# Open node with smallest domain size (use first, if multiple)
		current_node = this.graph.smallest_open_node(open_nodes)		
		if current_node == None:
			# graph passed AC3 at each step, i.e. all nodes are consistent and of domain >= 1
			# no node with domain > 1 found, i.e. all nodes are exactly 1 in size			
			return True
		
		# For AC3: only use constraints which might change == constraints involving at least one open node
		open_constraints = this.select_open_constraints()	
		# Reduce domains	
		if not this.apply_AC3(open_constraints):
			return False	
		
		# The algorithm will now try out all values in current_nodes's domain
		# AC3 was just applied, i.e. its domain is consistent with all neighbouring nodes
		# Backup must be generated, since deeper iterations might change this domain
		graph_backup = DomainGraph(this.graph) #stores a copy of all domains
		current_domain = copy.copy(current_node.domain)
		
		for value in current_domain:
			current_node.domain = {value}
			if this._search_solution(open_nodes):
				return True		

			# failed to find solution in this subtree, backtrack
			# but omit value just ruled out for current_node
			graph_backup.get_node(current_node.key).domain.remove(value)
			for node in this.graph.nodes:
				node.domain = graph_backup.get_node(node.key).domain

		return False
		
	# A generic way to output all node values in a found solution
	def display_solution(this):
		if this.solution_flag == None:
			print("No solution found yet")
		elif this.solution_flag == False:
			print("This problem is not satisfiable")
		else:
			for nd in this.graph.nodes:
				print("Node",nd.key,"-->",list(nd.domain)[0])

