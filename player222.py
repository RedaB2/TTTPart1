import sys
import math

###############################################################################
# GLOBAL CONSTANTS & RANDOM STUFF
###############################################################################

nameStr = "player222"

# Mapping from move strings (e.g., 'a1', 'b3') to (row, col)
move2Pos = {
    'a1': (0, 0), 'a2': (1, 0), 'a3': (2, 0),
    'b1': (0, 1), 'b2': (1, 1), 'b3': (2, 1),
    'c1': (0, 2), 'c2': (1, 2), 'c3': (2, 2),
}

# Reverse mapping for convenience (but not really following any particular style)
pos2Move = {v: k for k, v in move2Pos.items()}


def flipPlayer(playerVal):
    """Given 'X' returns 'O'; given 'O' returns 'X'."""
    return 'O' if playerVal == 'X' else 'X'


###############################################################################
# GAME STUFF
###############################################################################

def makeEmptyBoard():
    return [['.' for x in range(3)] for y in range(3)]


def winChecker(boardState):
    """
    Returns 'X' if X has a winning line, 'O' if O has a winning line, None otherwise.
    """
    rowLines = [''.join(boardState[i]) for i in range(3)]
    colLines = [''.join(boardState[r][j] for r in range(3)) for j in range(3)]
    diagLines = [
        boardState[0][0] + boardState[1][1] + boardState[2][2],
        boardState[0][2] + boardState[1][1] + boardState[2][0]
    ]

    allLines = rowLines + colLines + diagLines
    if 'XXX' in allLines:
        return 'X'
    if 'OOO' in allLines:
        return 'O'
    return None


def boardFull(boardState):
    """Return True if board is completely filled; otherwise False."""
    for i in range(3):
        for j in range(3):
            if boardState[i][j] == '.':
                return False
    return True


def terminalCheck(boardState):
    """
    Check if the board is in a terminal state (win or draw).
    """
    if winChecker(boardState) is not None:
        return True
    if boardFull(boardState):
        return True
    return False


def getAvailMoves(boardState):
    """Return a list of available moves as (row, col) tuples."""
    movesAvail = []
    for i in range(3):
        for j in range(3):
            if boardState[i][j] == '.':
                movesAvail.append((i, j))
    return movesAvail


def evalTerminalState(boardState, myMark):
    """
    Utility function:
      +100 if myMark wins,
      -100 if the opponent wins,
       0 for draw or non-terminal.
    """
    winRes = winChecker(boardState)
    if winRes is None:
        return 0
    return 100 if winRes == myMark else -100


def miniMaxAlphaBeta(boardState, depthLeft, a_val, b_val, isMax, myMark):
    """
    Alpha-beta minimax search.
    Returns a tuple (bestScore, bestMove).
    """
    if terminalCheck(boardState) or depthLeft == 0:
        return evalTerminalState(boardState, myMark), None

    currPlayer = myMark if isMax else flipPlayer(myMark)
    movesList = getAvailMoves(boardState)

    if not movesList:
        return evalTerminalState(boardState, myMark), None

    bestMoveFound = None

    if isMax:
        bestScore = -math.inf
        for (i, j) in movesList:
            boardState[i][j] = currPlayer
            score, _ = miniMaxAlphaBeta(boardState, depthLeft - 1, a_val, b_val, False, myMark)
            boardState[i][j] = '.'
            if score > bestScore:
                bestScore = score
                bestMoveFound = (i, j)
            a_val = max(a_val, bestScore)
            if a_val >= b_val:
                break  # beta pruning
        return bestScore, bestMoveFound
    else:
        bestScore = math.inf
        for (i, j) in movesList:
            boardState[i][j] = currPlayer
            score, _ = miniMaxAlphaBeta(boardState, depthLeft - 1, a_val, b_val, True, myMark)
            boardState[i][j] = '.'
            if score < bestScore:
                bestScore = score
                bestMoveFound = (i, j)
            b_val = min(b_val, bestScore)
            if b_val <= a_val:
                break  # alpha pruning
        return bestScore, bestMoveFound


def pickMyMove(boardState, myMark):
    """
    Choose a move using alpha-beta search (with a depth of 9).
    Returns the move in string format (e.g., 'b2').
    If no move is available, returns 'a1' as a fallback.
    """
    searchDepth = 9
    maxTurn = True  # our turn is always maximizing
    bestVal, moveRC = miniMaxAlphaBeta(boardState, searchDepth, -math.inf, math.inf, maxTurn, myMark)
    if moveRC is None:
        return "a1"  # fallback if terminal
    return pos2Move[moveRC]


def mainLoop():
    """
    Main entry point when running with the referee.
    """
    boardState = makeEmptyBoard()
    myMark = None

    for inLine in sys.stdin:
        inLine = inLine.strip()

        # Check if game ended
        if inLine.startswith("END:"):
            break

        if myMark is None:
            if inLine == "blue":
                myMark = 'X'
                chosenMove = pickMyMove(boardState, myMark)
                pos_r, pos_c = move2Pos[chosenMove]
                boardState[pos_r][pos_c] = myMark
                print(chosenMove, flush=True)
            elif inLine == "orange":
                myMark = 'O'
                continue
            else:
                continue
        else:
            if inLine in move2Pos:
                opp_r, opp_c = move2Pos[inLine]
                oppMark = flipPlayer(myMark)
                if boardState[opp_r][opp_c] == '.':
                    boardState[opp_r][opp_c] = oppMark
                if not terminalCheck(boardState):
                    nextMove = pickMyMove(boardState, myMark)
                    new_r, new_c = move2Pos[nextMove]
                    boardState[new_r][new_c] = myMark
                    print(nextMove, flush=True)
                else:
                    pass
            else:
                continue


###############################################################################
# OFFLINE TESTING (WHEN NOT USING THE REFEREE)
###############################################################################

def offlineTestRun():
    print("=== START TESTING ===")
    
    board_A = makeEmptyBoard()
    testMove1 = pickMyMove(board_A, "X")
    print("Test 1 (Empty board, X to move): returned move:", testMove1)

    board_B = [
        ['X', 'O', 'X'],
        ['.', 'O', '.'],
        ['.', '.', '.']
    ]
    testMove2 = pickMyMove(board_B, "X")
    print("Test 2 (Board B, X to move):", testMove2)

    board_C = [
        ['X', 'O', 'O'],
        ['X', '.', '.'],
        ['.', '.', '.']
    ]
    testMove3 = pickMyMove(board_C, "X")
    print("Test 3 (Board C, X can win):", testMove3)

    print("=== END TESTING ===")


if __name__ == "__main__":
    # Uncomment the next line to run offline tests
    # offlineTestRun()

    # Run with referee input:
    mainLoop()