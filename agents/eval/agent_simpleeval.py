# simple evaluation on all possible moves in the position

def agent_simpleeval(observation, configuration):

    # convert board to 2d
    board = [observation.board[i: i + configuration.columns] for i in range(0, len(observation.board), configuration.columns)]

    scores = []

    for move in range(configuration.columns):

        # column full, move not possible
        if observation.board[move] != 0:
            scores.append(float('-inf'))

        else:

            # simulate move
            for i in range(configuration.rows - 1, -1, -1):
                if board[i][move] == 0:
                    board[i][move] = observation.mark
                    break

            # evaluate position
            score = 0

            scores.append(score)

    return scores.index(max(scores))