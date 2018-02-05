import spacegame
import numpy as np

class Force:
    def __init__(self, xmagnitude, ymagnitude):
        self.xmagnitude = xmagnitude
        self.ymagnitude = ymagnitude

    def get_x_y(self):
        return np.array([self.xmagnitude, self.ymagnitude])

def createPointedForce(curr_loc, target_loc, scaling=1):
    # +-----
    # |0,0
    # |
    return Force((target_loc[0]-curr_loc[0]) * scaling, (target_loc[1]-curr_loc[1]) * scaling)

