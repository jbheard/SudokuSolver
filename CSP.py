from collections import deque

'''
Code based on AI: A Modern Approach, 3rd Ed. p.209
'''
class CSP:
	# Set arcs between variables, where each arc is in the format (i, j, k, ...) for X[i], X[j], X[k] respectively
	# Each arc must have a minimum of 2 variables
	def __init__(self, X, D, C, arcs=None):
		assert len(X) == len(D), "Must have domain for each variable"
		assert len(C) > 0, "Require at least 1 constraint "
		self.X = X
		self.D = D
		self.C = C
		self.arcs = None if arcs is None else arcs[:]
		return

	# Creates and returns a copy of the current csp
	def copy(self):
		if self.arcs:
			new_csp = CSP(self.X[:], [d[:] for d in self.D], self.C[:], self.arcs[:])
		else:
			new_csp = CSP(self.X[:], [d[:] for d in self.D], self.C[:])
		return new_csp

	# Returns a list of arcs between variables within the CSP
	# Returns None if no arcs are assigned
	def get_arcs(self):
		assert self.arcs is not None, "Method requires arcs"
		return self.arcs[:]

	# Returns a list of arcs adjacent to X[i] (all arcs which include X[i])
	def neighbors(self, i):
		assert self.arcs is not None, "Method requires arcs"
		neighbors = list(filter(lambda x: i in x, self.arcs))
		return neighbors

	# Evaluate all binary constraint of given arguments
	def evaluate_constraints(self, *args):
		val = any(c(args) for c in self.C)
		return val

	# Evaluates constraints on all arcs
	def evaluate_arc_constraints(self):
		assert self.arcs is not None, "Method requires arcs"
		val = any( c( (self.X[a[0]], self.X[a[1]]) ) for c in self.C for a in self.arcs )
		return val

	# Implementation of AC3 to enforce arc consistency and prune solution search space
	def AC3(self):
		assert self.arcs is not None, "Method requires arcs"
		#queue = deque(self.get_arcs())
		queue = self.get_arcs()
		while len(queue) > 0:
			i, j = queue.pop()
			if self.revise(i, j):
				if len(self.D[i]) == 0: # Domain must have @ least 1 value
					return False
				for k in self.neighbors(i):
					if k == (i,j): 		# Skip current arc
						continue
					if k not in queue: 	# Insert arc
						queue.append( k )
		return True

	# Revise function to remove invalid values from domains
	def revise(self, i, j):
		assert self.arcs is not None, "Method requires arcs"
		if len(self.D[j]) == 1:
			if self.D[j][0] in self.D[i]:
				self.D[i].remove(self.D[j][0])
				return True
		return False

