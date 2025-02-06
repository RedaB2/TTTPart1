import sys
import math

###############################################################################
# GLOBAL CONSTANTS & UTILITIES
###############################################################################

NAME = "Unstoppable"

# Map move strings (e.g., 'a1', 'b3') to (row, col)
MAPMOVCOORD = {
    'a1': (0, 0), 'a2': (1, 0), 'a3': (2, 0),
    'b1': (0, 1), 'b2': (1, 1), 'b3': (2, 1),
    'c1': (0, 2), 'c2': (1, 2), 'c3': (2, 2),
}

# Reverse mapping for convenience
COORD_TO_MOVE = {v: k for k, v in MAPMOVCOORD.items()}

def opposite_player(symbol):
    """Given 'X' returns 'O'; given 'O' returns 'X'."""
    return 'O' if symbol == 'X' else 'X'


###############################################################################
# GAME LOGIC
###############################################################################

def create_empty_board():
    return [['.' for _ in range(3)] for _ in range(3)]

def check_winner(board):
    """
    Returns 'X' if X has a winning line, 'O' if O has a winning line, None otherwise.
    """
    rows = [''.join(board[r]) for r in range(3)]
    cols = [''.join(board[r][c] for r in range(3)) for c in range(3)]
    diags = [
        board[0][0] + board[1][1] + board[2][2],
        board[0][2] + board[1][1] + board[2][0]
    ]

    lines = rows + cols + diags
    if 'XXX' in lines:
        return 'X'
    if 'OOO' in lines:
        return 'O'
    return None

def board_is_full(board):
    """Return True if no '.' found, else False."""
    for r in range(3):
        for c in range(3):
            if board[r][c] == '.':
                return False
    return True

def is_terminal(board):
    """
    Check if the board is ful (draw) or win.
    """
    if check_winner(board) is not None:
        return True
    if board_is_full(board):
        return True
    return False

def get_legal_moves(board):
    """List of positions that are open and legal."""
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == '.':
                moves.append((r, c))
    return moves


def evaluate_terminal(board, my_symbol):
    """
    utility function
      +100 if my_symbol has won
      -100 if the opponent has won
       0 if draw or no winner
    """
    winner = check_winner(board)
    if winner is None:
        return 0  # no winner or draw
    return 100 if winner == my_symbol else -100

def alpha_beta_minimax(board, depth, alpha, beta, maximizing, my_symbol):
    """
    alpha beta min-max --> 
    Returns (best_value, best_move).
    """
    if is_terminal(board) or depth == 0:
        return evaluate_terminal(board, my_symbol), None

    active_player = my_symbol if maximizing else opposite_player(my_symbol)
    legal_moves = get_legal_moves(board)

    if not legal_moves:
        # is board full? 
        return evaluate_terminal(board, my_symbol), None

    best_move = None

    if maximizing:
        value = -math.inf
        for (r, c) in legal_moves:
            board[r][c] = active_player
            child_val, _ = alpha_beta_minimax(board, depth - 1, alpha, beta,
                                              False, my_symbol)
            board[r][c] = '.'
            if child_val > value:
                value = child_val
                best_move = (r, c)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta prune
        return value, best_move

    else:
        value = math.inf
        for (r, c) in legal_moves:
            board[r][c] = active_player
            child_val, _ = alpha_beta_minimax(board, depth - 1, alpha, beta,
                                              True, my_symbol)
            board[r][c] = '.'
            if child_val < value:
                value = child_val
                best_move = (r, c)
            beta = min(beta, value)
            if beta <= alpha:
                break  # alpha prune
        return value, best_move


def choose_move(board, my_symbol):
    """
    Decide which move to make using alpha-beta search (depth = 9).
    Return the move in string form, e.g., 'b2'.
    If no possible move (terminal state), return 'a1' just as a placeholder.
    """
    depth_limit = 9
    maximizing = True  # we always treat our own turn as "maximizing"

    best_value, best_rc = alpha_beta_minimax(board, depth_limit,
                                             -math.inf, math.inf,
                                             maximizing, my_symbol)
    if best_rc is None:
        # terminal?
        return "a1"  # fallback

    return COORD_TO_MOVE[best_rc]


def main():
    """
    ENTRY POINT FOR REFEREE
    """
    board = create_empty_board()
    my_symbol = None

    for line in sys.stdin:
        line = line.strip()

        # status of the game?
        if line.startswith("END:"):
            # no more moves
            break

        if my_symbol is None:
            # blue or orange from ref
            if line == "blue":
                my_symbol = 'X'
                # we are first player => make an immediate move
                move_str = choose_move(board, my_symbol)
                
                r, c = MAPMOVCOORD[move_str]
                board[r][c] = my_symbol
                
                print(move_str, flush=True)

            elif line == "orange":
                my_symbol = 'O'
                continue

            else:
                continue

        else:
            if line in MAPMOVCOORD:
                (opp_r, opp_c) = MAPMOVCOORD[line]
                opp_symbol = opposite_player(my_symbol)

            
                if board[opp_r][opp_c] == '.':
                    board[opp_r][opp_c] = opp_symbol

                
                if not is_terminal(board):
                    move_str = choose_move(board, my_symbol)
                    
                    rr, cc = MAPMOVCOORD[move_str]
                    board[rr][cc] = my_symbol

                    print(move_str, flush=True)
                else:
                    pass

            else:
                continue


###############################################################################
# TESTING (IF REFEREE ISNT USED)
###############################################################################

def run_offline_tests():
    print("=== START TESTING ===")

    board1 = create_empty_board()
    move1 = choose_move(board1, "X")
    print("Test 1 (Empty board, X to move): returned move:", move1)

    board2 = [
        ['X', 'O', 'X'],
        ['.', 'O', '.'],
        ['.', '.', '.']
    ]
    move2 = choose_move(board2, "X")
    print("Test 2 (Board2, X to move):", move2)

    board3 = [
        ['X', 'O', 'O'],
        ['X', '.', '.'],
        ['.', '.', '.']
    ]
    move3 = choose_move(board3, "X")
    print("Test 3 (Board3, X can win):", move3)

    print("=== END TESTING ===")


if __name__ == "__main__":
    # uncomment this line for testing
    #run_offline_tests()

    # For referee-based play:
    main()