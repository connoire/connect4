# function to get distance from middle columns
def GetDistance(observation, configuration):

    distances = {}

    # calculate distance from centre column
    for j in range(configuration.columns):
        dist = abs(j - (configuration.columns - 1) / 2)

        # add to dictionary
        for i in range(configuration.rows):
            distances[(i, j)] = -dist

    return distances

# function to get all windows of winning length in the board
def GetWindows(observation, configuration): 

    # get all wining length windows across the whole board
    windows = []
    dirs = [(1, 1), (1, 0), (0, 1), (1, -1)]

    for x in range(configuration.rows):
        for y in range(configuration.columns):

            for dx, dy in dirs:
                window = set([(x + i * dx, y + i * dy) for i in range(configuration.inarow)])

                # check out of bounds
                if all(0 <= i and i < configuration.rows and 0 <= j and j < configuration.columns for i, j in window):
                    windows.append(window)

    return windows

# function to get location of all player and opponent checkers
def GetLocations(observation, configuration):

    empty = set()
    ply = set()
    opp = set()

    # convert board to 2d
    board = [observation.board[i: i + configuration.columns] for i in range(0, len(observation.board), configuration.columns)]

    # iterate over board
    for i in range(configuration.rows):
        for j in range(configuration.columns):
            
            cell = board[i][j]

            # empty cell
            if cell == 0:
                empty.add((i, j))
            
            # player checker
            elif cell == observation.mark:
                ply.add((i, j))
            
            # opponent checker
            else:
                opp.add((i, j))

    return empty, ply, opp

# function to score the window based on number of checkers player and opponent owns
def ScoreWindow(observation, configuration, plycount, oppcount):

    # locked window
    if plycount > 0 and oppcount > 0:
        return 0

    # empty window
    if plycount == 0 and oppcount == 0:
        return 0

    # player owned window, weight higher if player has more
    if oppcount == 0:
        return 5 ** plycount
    
    # opponent owned window, weight higher if opponent has more
    else:
        return -5 ** oppcount


# function to evaluate every cell based on number of checkers in its windows
def EvaluateWindows(observation, configuration, evaluation, windows, ply, opp):

    evaluation = evaluation.copy()

    # iterate over every window
    for window in windows:

        # count number of cells player and oppnent owns
        plycount = 0
        oppcount = 0

        # look through every cell in window
        for (i, j) in window:
            
            if (i, j) in ply:
                plycount += 1
            elif (i, j) in opp:
                oppcount += 1

        score = ScoreWindow(observation, configuration, plycount, oppcount)

        # add score to every cell in window
        for (i, j) in window:
            evaluation[(i, j)] += score

    return evaluation

# simple evaluation on all possible moves in the position
def agent_simpleeval(observation, configuration):

    # find all possible moves (column not filled up)
    possible = []
    for i in range(configuration.columns):
        if observation.board[i] == 0:
            possible.append(i)

    # get all windows of winning length
    windows = GetWindows(observation, configuration)

    # get locations of all player and opponent checkers
    empty, ply, opp = GetLocations(observation, configuration)

    # initialise evaluation with distance from middle columns
    evaluation = GetDistance(observation, configuration)

    # add window evaluation
    evaluation = EvaluateWindows(observation, configuration, evaluation, windows, ply, opp)

    # find best move
    bestscore = float('-inf')
    bestmove = None
    for move in possible:

        # find row of move
        for i in range(configuration.rows - 1, -1, -1):
            if (i, move) in empty:
                break

        score = evaluation[(i, move)]

        if score > bestscore:
            bestscore = score
            bestmove = move

    return bestmove