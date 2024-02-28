from utils import h_compute
import numpy as np
import copy
from line_profiler_pycharm import profile


def select_task(c, x, y, J, z, i):
    if sum(x) == 0:  # If the agent is not assigned a task
        h = h_compute(c, y)  # Valid task list
        if sum(h) != 0:  # If there are valid tasks
            max_valid_c = -1
            # Find the highest bid for a valid task and its index
            for j in range(len(y)):
                if h[j] == 1 and c[j] > max_valid_c:
                    J = j
                    max_valid_c = c[j]
            # Select the highest bid task and update the winning bid list and the highest bid estimate
            x[J] = 1
            z[J] = i
            y[J] = c[J]
    return x, y, J, z


# @profile
def update_task(g, y, J, x, i, z, c):
    new_y = [row[:] for row in y]
    # Update the agent's maximum bid for the task using neighbor information
    for j in range(len(y[0])):
        for k in range(len(g)):
            if g[k] == 1:
                if y[k][j] > new_y[i][j]:
                    new_y[i][j] = y[k][j]

    max_y = y[i][J[i]]
    # Update the list of winning bids using neighbor information
    for k in range(len(g)):
        if g[k] == 1:
            if y[k][J[i]] > max_y:
                z[i][J[i]] = k
                max_y = y[k][J[i]]

    # Update the task selection for this agent using the winning bid list
    if z[i][J[i]] != i:
        x[J[i]] = 0

    """
    When multiple agents bid the same price for the same task, the task is assigned to the agent with the largest index
    """
    for k in range(len(g)):
        for j in range(len(y[0])):
            if g[k] == 1:
                if z[k][j] > z[i][j] and c[k][j] == c[i][j]:
                    if J[i] == j:
                        x[j] = 0
                    z[i][j] = z[k][j]

    return x, new_y, J[i], z
