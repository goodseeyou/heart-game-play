import random
import Action


class NeuralNetwork:
    def __init__(self):
        pass

    def predict(self, game_instance_array):
        action = Action.FALSE_ACTION_INSTANCE[:]
        for i in range(Action.LEN_ACTION_CANDIDATE):
            action[i] = random.randint(0, 10000) / 10000.0

        v = random.randint(-1000, 1000) / 1000.0

        return action, v
