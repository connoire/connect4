# completely random move (only on non-filled columns)

def agent_rand(observation, configuration):

    from random import choice
    return choice([c for c in range(configuration.columns) if observation.board[c] == 0])