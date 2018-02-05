import spacegame

def createPointedForce(curr_loc, target_loc, scaling=1):
    # +-----
    # |0,0
    # |
    return Force((target_loc[0]-curr_loc[0]) * scaling, (target_loc[1]-curr_loc[1]) * scaling)
