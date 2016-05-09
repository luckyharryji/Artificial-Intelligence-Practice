from SudokuStarter import *

sb = init_board("input_puzzles/easy/25_25.sudoku")
sb.print_board()

fb = solve(sb, True, False, False, False)

fb.print_board()
