import numpy as np
from CBAA import select_task, update_task
import copy
from line_profiler_pycharm import profile
import random

# @profile
def CBAA_main(N_a, N_t, c, g):
    """
    Based on the thesis "Consensus-Based Decentralized Auctions for Robust Task Allocation", the realization of
    consensus-based auction algorithm (CBAA) is presented
    :param N_a: The number of agents
    :param N_t: The number of tasks
    :param c:   Bid
    :param g:   Communication adjacency matrix, its value of 1 can communicate, otherwise it cannot
    :return:    The task allocation in each iteration
    """
    x = [[0 for _ in range(N_t)] for _ in range(N_a)]  # Agent's task list
    y = [[-1 for _ in range(N_t)] for _ in range(N_a)]  # Latest estimates of the highest bid per task
    J = [None for _ in range(N_a)]  # Stores the task currently selected by the agent
    z = [[-1 for _ in range(N_t)] for _ in range(N_a)]  # Each agent's own list of winning bids
    x_history = []

    # Cycle through the task selection step and task update step of CBAA
    while True:
        for i in range(N_a):
            x[i], y[i], J[i], z[i] = select_task(c[i], x[i], y[i], J[i], z[i], i)
            x[i], y, J[i], z = update_task(g[i], y, J, x[i], i, z, c)
        x_history.append(copy.deepcopy(x))
        if np.all(np.sum(x, axis=0) == 1):  # Until all tasks are assigned, out of the loop
            break

    return x_history


# Example
if __name__ == "__main__":
    N_a = 3
    N_t = 3
    c = [[random.random() for _ in range(N_t)] for _ in range(N_a)]
    g = [[1 for _ in range(N_t)] for _ in range(N_a)]
    x_history = CBAA_main(N_a, N_t, c, g)  # Run CBAA to get the task allocation in each iteration
    print(x_history[-1])  # Display allocation results
