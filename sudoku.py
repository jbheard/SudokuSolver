import CSP
from math import sqrt

# Dimension of the sudoku puzzle
DIM = 9
# For counting number of attempts made in backtracing search
cnt = 0

# Constraint on a set of values; 
# True iff all values > 0 are distinct
def alldiff(X):
	s = set(X) - set([0])
	return len(s) == len([x for x in X if x != 0])

# Return stats on the backtrack search
def get_cnt():
	return cnt
	
# Read a sudoku puzzle from a file
# NOTE: This method does not scale beyond 9x9 puzzles
def read_sudoku(file):
	sudoku = []
	lineno = 0
	for line in file:
		# Remove spaces and error check
		line = ''.join(line.split())
		if len(line) == 0:
			continue
		elif len(line) != DIM:
			raise ValueError("incorrect number of values on line %d" % (lineno))
		elif not line.isdigit():
			raise ValueError("invalid value at line %d" % (lineno))

		# Get each digit in the line
		for num in line:
			sudoku.append( int(num) )

		# Only read first 9 lines
		lineno += 1
		if lineno == DIM: 
			break

	return sudoku

# Write a sudoku puzzle to a file (from CSP object)
def write_sudoku(file, assignment):
	for i in range(DIM):
		# Generate format string for a row
		s = "{} " * DIM
		# Fill in the formatting with fancy python magic
		s = s.format(*(assignment[i*DIM:(i+1)*DIM]))
		# Write the row to the file
		print(s, file=file)
	return

# Converts one large arc into a set of binary arcs
def binary_arcs(arc):
	combos = []
	# For every pair (i, j) make an arc (i, j)
	for i in range(len(arc)):
		for j in range(len(arc)):
			if i == j: continue # Ignore all cases where i == j
			combos.append( (arc[i], arc[j]) )
	return combos

# Create a new CSP for a sudoku puzzle
def new_sudoku(file=None):
	if not file:
		# Create empty sudoku with domains 1-9 for every cell
		X = [0] * DIM*DIM
		D = [ list(range(1,DIM+1)) for _ in range(len(X)) ]
	else:
		# Read a sudoku and fill in domain values
		X = read_sudoku(file)
		D = []
		for i in range(len(X)):
			if X[i] == 0:
				D.append( list(range(1,DIM+1)) )
			else:
				D.append( [ X[i] ] )
	# Only one constraint to satisfy (on a variety of arcs)
	C = [ alldiff ]
	# Seems like it could be done more correctly

	# Generate all rows, columns, and boxes
	box_size = int(sqrt(DIM))
	rows, cols, boxes = [], [], []
	for i in range(0,DIM):
		row, col, box = [], [], []
		for j in range(0,DIM):
			row.append(i + DIM*j)
			col.append(DIM*i + j)
			box.append( (j%box_size) + DIM*(j//box_size) + box_size*(i%box_size) + DIM*box_size*(i//box_size) )
		rows.append(tuple(row))
		cols.append(tuple(col))
		boxes.append(tuple(box))

	# Convert all groups into binary arcs
	groups = rows + cols + boxes
	arcs = []
	for group in groups:
		arcs += binary_arcs(group)

	# Return a CSP representation of the sudoku
	return CSP.CSP(X, D, C, arcs)

# Function from textbook, choose the next value to work on
# Uses Minimum-Remaining-Value heuristic (attempt to cause collision faster, decrease branching factor)
def select_unassigned_variable(csp):
	min = DIM+1
	index = 0
	for i in range(len(csp.X)):
		if csp.X[i] == 0 and len(csp.D[i]) < min:
			index = i
			min = len(csp.D[i])
	return index

# Least-Constraining-Value heuristic (prioritizes neighboring variable with most available choices)
def order_domain_values(csp,var):
	if len(csp.D[var]) == 1:
		return csp.D[var]
	return sorted(csp.D[var], key=lambda val: compares(csp, var, val))

# Comparison function, helper to order_domain_values
def compares(csp,var,val):
	count = 0
	for n in csp.neighbors(var):
		if len(csp.D[n[0]]) > 1 and val in csp.D[n[0]]:
			count += 1
	return count

# Get inferences on variable
def inferences(csp, var):
	revise = lambda x: csp.revise(*x)
	# Revise all neighbors of the given variable
	neighbors = csp.neighbors(var)
	res = list(map(revise, neighbors))
	
	for i in range(len(res)):
		# If there is a change
		if res[i]:
			index = neighbors[i][0]
			# If the change results in an empty domain
			if len(csp.D[index]) == 0:
				return False # Return failure
	return True # Return success

# Backtracing search for a solution on a csp
# returns assignment  if solvable,
# returns None        otherwise
def backtrack(csp):
	global cnt
	cnt = 0
	assignment = []
	for i in range(len(csp.D)):
		# If a domain only has one value, it has to be in the assignment
		if len(csp.D[i]) == 1:
			assignment.append(csp.D[i][0])
			csp.X[i] = csp.D[i][0]
		# Variables with multiple possibilities are set to 0
		else:
			assignment.append(0)
	# Perform the actual search
	res = backtrack_help(assignment, csp)
	return res

# Recursive helper method for backtrack, based on textbook
def backtrack_help(assignment, csp):
	global cnt
	# var = SELECT-UNASSIGNED-VARIABLE(csp)
	#var = select_unassigned_variable(csp)
	if 0 in assignment:
		var = select_unassigned_variable(csp)
	elif csp.evaluate_arc_constraints():
		return assignment
	else:
		return None

	# for value in ORDER-DOMAIN-VALUES(...)
	for value in order_domain_values(csp,var):
		# Add {var = value} to assignment
		old = csp.X[var]
		assignment[var] = value
		csp.X[var] = value

		if csp.evaluate_arc_constraints(): # if value consistent with assignment
			# If the assignment is evaluated as correct and 
			new_csp = csp.copy()
			new_csp.D[var] = [ value ]
			
			if inferences(new_csp, var): # if inferences != failure
				cnt += 1
				# recursive call
				result = backtrack_help(assignment[:], new_csp)
				if result is not None:
					return result
		# remove {var = value} and inferences from assignment
		csp.X[var] = old
		assignment[var] = 0
	# Attempted all values, no solution found
	return None

