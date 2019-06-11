import sys
from sudoku import read_sudoku, DIM

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: {} sudoku1 sudoku2".format(sys.argv[0]), file=sys.stderr)
		print()
		print("checks if two sudokus match. That is, check that every cell matches, or ignore if the cell is 0.")
		exit(1)
	try:
		# Open the two files
		f1 = open(sys.argv[1], 'r')
		f2 = open(sys.argv[2], 'r')
		
		# Read the puzzles
		s1 = read_sudoku(f1)
		s2 = read_sudoku(f2)
		
		# Close the files
		f1.close()
		f2.close()
		
		# Check every cell
		for i in range(len(s1)):
			# Ignore 0s
			if s1[i] == 0 or s2[i] == 0:
				continue
			# Check for equality
			if s1[i] != s2[i]:
				print("False")
				exit(0)
		
		# We made it here! They are equal
		print("True")
	except FileNotFoundError as e:
		print("Error opening file: " + str(e))
		exit(1)
	