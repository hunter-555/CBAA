def h_compute(c, y):
    h = [0 for _ in range(len(c))]
    # The task is valid when the bid is higher than the current estimated bid
    for j in range(len(c)):
        if c[j] > y[j]:
            h[j] = 1
        else:
            h[j] = 0
    return h