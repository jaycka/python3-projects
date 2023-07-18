import numpy as np


class GameBrain:
    def __init__(self):
        self.available = np.empty([3, 3])
        self.available[:] = np.nan

    def computer_turn(self, value: bool) -> tuple:
        row = np.random.choice(range(self.available.shape[0]))
        col = np.random.choice(range(self.available.shape[0]))
        while str(self.available[row, col]) != str(np.nan):
            row = np.random.choice(range(self.available.shape[0]))
            col = np.random.choice(range(self.available.shape[0]))
        self.available[row, col] = not value
        return row, col

    def check_result(self, value: bool) -> bool:
        current = self.available == value
        column_sum = np.sum(current, axis=0)
        row_sum = np.sum(current, axis=1)
        if (3 in column_sum) or (3 in row_sum) or (current[0, 0] == current[1, 1] == current[2, 2] == True) or (
                np.rot90(current)[0, 0] == np.rot90(current)[1, 1] == np.rot90(current)[2, 2] == True):
            return True
        else:
            return False

    def reset(self):
        self.available = np.empty([3, 3])
        self.available[:] = np.nan
