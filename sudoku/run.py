from SudokuStarter import *

sb = init_board("input_puzzles/easy/25_25.sudoku")
sb.print_board()

fb = solve(sb, True, True, False, True)

fb.print_board()
