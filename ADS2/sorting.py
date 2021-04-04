def countingsort(array, lowerbound, upperbound):
    sorted_array = []
    count = {}
    for elem in array:
        if elem in count:
            count[elem] += 1
        else:
            count[elem] = 1
    for elem in range(lowerbound, upperbound + 1):
        if elem in count:
            sorted_array.extend([elem] * count[elem])

    return sorted_array


def count_sort(array, col):
    output = [0] * len(array)
    count = [0] * (52 + 1)  # One addition cell to account for dummy letter
    min_base = ord('a') - 1  # subtract one too allow for dummy character

    for item in array:  # generate Counts
        # get column letter if within string, else use dummy position of 0
        letter = ord(item[col]) - min_base if col < len(item) else 0
        count[letter] += 1

    for i in range(len(count) - 1):  # Accumulate counts
        count[i + 1] += count[i]

    for item in reversed(array):
        # Get index of current letter of item at index col in count array
        letter = ord(item[col]) - min_base if col < len(item) else 0
        output[count[letter] - 1] = item
        count[letter] -= 1

    return output


def radixsort(names):
    max_col = -1
    for name in names:
        max_col = max(max_col, len(name))
    # max_col = len(max(names, key=len))
    for col in range(max_col - 1, -1, -1):
        names = count_sort(names, col)

    return names


def partition(arr, pivot_index):
    n = len(arr)

    arr[0], arr[pivot_index] = arr[pivot_index], arr[0]

    current_position = 0

    for i in range(1, n):  # Partitioning loop
        if arr[i] <= arr[0]:
            current_position += 1
            arr[i], arr[current_position] = arr[current_position], arr[i]

    arr[0], arr[current_position] = arr[current_position], arr[0]

    return arr


def quicksort(arr):
    n = len(arr)

    # Base case
    if n < 2:
        return arr

    current_position = 0  # Position of the partitioning element

    for i in range(1, n):  # Partitioning loop
        if arr[i] <= arr[0]:
            current_position += 1
            arr[i], arr[current_position] = arr[current_position], arr[i]

    arr[0], arr[current_position] = arr[current_position], arr[0]  # Brings pivot to it's appropriate position

    left = quicksort(arr[0:current_position])  # Sorts the elements to the left of pivot
    right = quicksort(arr[current_position + 1:n])  # sorts the elements to the right of pivot

    arr = left + [arr[current_position]] + right  # Merging everything together

    return arr

if __name__ == '__main__':
    # arr = [3, 2, 1]
    # lowerbound = 1
    # upperbound = 3
    # #  [1, 2, 3]
    # print(countingsort(arr, lowerbound, upperbound))
    #
    # arr = []
    # lowerbound = 0
    # upperbound = 10
    # # []
    # print(countingsort(arr, lowerbound, upperbound))
    #
    # arr = [5, 2]
    # lowerbound = 2
    # upperbound = 5
    # # [2, 5]
    # print(countingsort(arr, lowerbound, upperbound))

    # arr = ['Ivan', 'John', 'Anna']
    # arr.sort()
    # # ['Anna', 'Ivan', 'John']
    # print(radixsort(arr))

    arr = [3508, 3706, 9536, 5129, 168]
    print(partition(arr, 3))
    print(quicksort(arr))