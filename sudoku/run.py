from SudokuStarter import *

sb = init_board("input_puzzles/easy/9_9.sudoku")
sb.print_board()

fb = solve(sb, True, False, False, True, False)

fb.print_board()
