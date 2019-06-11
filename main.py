from sudoku import new_sudoku, write_sudoku, backtrack, get_cnt
from time import process_time
import sys


# Main program to test sudoku CSP
if __name__ == '__main__':
	file = open(input("fname: "), 'r')
	csp = new_sudoku(file)
	file.close()
	
	# Print the result of AC3
	ac3 = csp.AC3()
	print("AC3: {}".format(ac3))
	for d in csp.D: # Print AC3 reduced domains
		print("   {}".format(d))

	# Ac3 failed, no solutions
	if not ac3:
		print("The puzzle has no solutions")
		exit(0)
		
	# Perform backtracing algorithm to find solution
	time_ = process_time() # Measure the time in seconds
	result = backtrack(csp)
	time_ = process_time() - time_

	# Show timing results
	print("Took {:.2f} seconds".format(time_))
	print("Finished on attempt {}".format(get_cnt()))

	# Show no solutions
	if result is None:
		print("The puzzle has no solutions")
		exit(0)
	
	write_sudoku(sys.stdout, result)
	ans = input("Save solution? (Y/n) ")
	if ans.lower() != 'y': exit(0)
	
	# Save the solution to a file
	file = open(input("fname: "), 'w')
	write_sudoku(file, csp)
	file.close()
