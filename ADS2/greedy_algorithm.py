def teamOracle(team_size, start_times, finish_times):
    # raise Exception([team_size, start_times, finish_times])
    available = team_size
    tasks = [(x, y) for x, y in zip(start_times, finish_times)]
    tasks.sort(key=lambda x: x[0])
    in_work = []

    for task in tasks:
        # are there finished
        for job in in_work:
            if task[0] > job[1]:
                in_work.remove(job)
                available += 1
        if available > 0:
            in_work.append(task)
            available -= 1
        else:
            return False

    return True


def minRestarts(m, t, no_request_times):
    min_restarts = 0
    current = 0
    no_request_times = set(no_request_times)

    # corner case
    if t >= m:
        return 0

    while current < m:
        advanced = False
        for step in range(t, 0, -1):
            if current + step >= m:
                return min_restarts
            if current + step in no_request_times:
                current += step + 1
                min_restarts += 1
                advanced = True
                break
        if not advanced:
            return -1

    return min_restarts


def minUnionCost(set_sizes):
    n = len(set_sizes)
    min_sum = 0

    while len(set_sizes) > 1:
        set_sizes.sort()
        num_1 = set_sizes.pop(0)
        num_2 = set_sizes.pop(0)
        set_sizes.append(num_1 + num_2)
        min_sum += num_1 + num_2

    return min_sum

if __name__ == '__main__':
    # team_size = 9
    # start_times = [6, 10, 3, 1, 10, 1, 6, 20, 1, 12, 5, 1, 5, 6, 5, 7, 1, 13]
    # finish_times = [11, 15, 18, 19, 17, 10, 16, 21, 1, 21, 9, 10, 10, 11, 6, 11, 19, 15]
    #
    # print(teamOracle(team_size, start_times, finish_times))

    # m = 91
    # t = 10
    # no_request_times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86, 87, 88, 89, 90, 91]
    # print(minRestarts(m, t, no_request_times))

    set_sizes = [2, 6]
    print(minUnionCost(set_sizes))


