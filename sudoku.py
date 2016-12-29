from CSPmain import *


def different(x,y):
	return x != y

# Adds some additional functionality to Graph for initialization
class Sudoku(Graph):
	def __init__(this):
		Graph.__init__(this)
		dom = {1,2,3,4,5,6,7,8,9}
		
		#creates nodes 
		for row in range(9):
			for col in range(9):
				new_node = Node((row+1,col+1),dom)
				this.add_node(new_node)
				
		#create constraints, no double numbers in each row
		for row in range(9):
			entries = []
			for col in range(9):
				entries.append((row+1,col+1))
				this.new_constraint(different,entries,"mutual")
				
		#create constraints, no double numbers in each column
		for col in range(9):
			entries = []
			for row in range(9):
				entries.append((row+1,col+1))
				this.new_constraint(different,entries,"mutual")
						
		#create constraints, no double numbers in each box
		for box in range(9):
			entries = []
			for ent in range(9):
				row = 3*(box//3)+ent//3 + 1
				col = 3*(box%3)+ent%3 + 1
				entries.append((row,col))
				this.new_constraint(different,entries,"mutual")
	
	# read in Sudoku known values from file					
	def read_in_matrix(this,filename):
		import csv		
		col = 0
		row = 0
		with open(filename, 'rt') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for line in reader:
				if line != []:
					row += 1
				col = 0
				for entry in line:
					col += 1
					if len(entry) > 1:
						entry = entry[1]
					if str.isdigit(entry):
						value = int(entry)
						this.set_value((row,col),value)
	
	def display_sudoku(this,solver):
		if solver.solution_flag == None:
			print("No solution found yet")
		elif solver.solution_flag == False:
			print("This problem is not satisfiable")
		else:
			for row in range(9):
				if row % 3 == 0:
					print("")			
				values = [list(this.get_node((row+1,col+1)).domain)[0] for col in range(9)]
				print("%d %d %d   %d %d %d   %d %d %d" %tuple(values))			
	
		

###
S = Sudoku()

# read in external file
S.read_in_matrix("sudoku3.txt")	


# solve Sudoku
X = Solver(S)
X.search_solution()
X.graph.display_sudoku(X)
