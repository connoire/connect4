# fills board from left to right

def agent_fill(observation, configuration):

    for c in range(configuration.columns):
        if observation.board[c] == 0:
            return c