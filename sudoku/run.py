from SudokuStarter import *

sb = init_board("input_puzzles/more/16x16/16x16.20.sudoku")
sb.print_board()

fb = solve(sb, True, True, False, False)

fb.print_board()
