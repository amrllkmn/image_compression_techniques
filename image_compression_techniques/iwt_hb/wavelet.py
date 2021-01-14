import numpy as np


def _iwt(array):

    nx, ny = array.shape
    if nx % 2 != 0 and ny % 2 == 0:
        # Add row
        extra = array[0, :]
        array = np.insert(array, nx, extra, axis=0)
        nx = array.shape[0]

    elif ny % 2 != 0 and nx % 2 == 0:
        # Add column
        extra = array[:, 0]
        array = np.insert(array, ny, extra, axis=1)
        ny = array.shape[1]

    elif nx % 2 != 0 and ny % 2 != 0:
        extra_row = array[0, :]
        extra_col = array[:, 0]
        array = np.insert(array, nx, extra_row, axis=0)
        nx = array.shape[0]
    output = np.zeros_like(array)
    x = nx//2

    for j in range(ny):
        output[0:x, j] = (array[0::2, j] + array[1::2, j])//2
        output[x:nx, j] = array[0::2, j] - array[1::2, j]

    return output


def _iiwt(array):
    # print(array.shape)
    nx, ny = array.shape
    if nx % 2 != 0 and ny % 2 == 0:
        # Add row
        extra = array[0, :]
        array = np.insert(array, nx, extra, axis=0)
        nx = array.shape[0]

    elif ny % 2 != 0 and nx % 2 == 0:
        # Add column
        extra = array[:, 0]
        array = np.insert(array, ny, extra, axis=1)
        ny = array.shape[1]

    elif nx % 2 != 0 and ny % 2 != 0:
        extra_row = array[0, :]
        extra_col = array[:, 0]
        array = np.insert(array, nx, extra_row, axis=0)
        nx = array.shape[0]

    output = np.zeros_like(array)
    x = nx//2
    for j in range(ny):
        output[0::2, j] = array[0:x, j] + (array[x:nx, j] + 1)//2
        output[1::2, j] = output[0::2, j] - array[x:nx, j]

    return output


def iwt2(array):
    return _iwt(_iwt(array.astype(int)).T).T


def iiwt2(array):
    return _iiwt(_iiwt(array.astype(int).T).T)


def iwt4(array):
    return _iwt(_iwt(_iwt(_iwt(array.astype(int)).T).T).T).T


def non_zero_mapping(array):
    y_cap = np.zeros(array.shape)

    y_cap[1:] = array[0:len(array)-1]

    diff = array - y_cap

    y_max = max(array)
    y_min = min(array)

    Ti = np.zeros(array.shape)

    output = np.zeros(array.shape)

    for i in range(len(y_cap)):
        Ti[i] = min(y_max - y_cap[i], y_cap[i] - y_min)

        if 0 <= diff[i] <= Ti[i]:
            output[i] = 2 * diff[i]
        elif -1-Ti[i] <= diff[i] < 0:
            output[i] = 2 * abs(diff[i])
        else:
            output[i] = Ti[i] + abs(diff[i])

    return output


def other_zero_mapping(array):

    output = np.zeros(array.shape, dtype=int)

    y_min = min(array)
    for i in range(len(array)):
        delta = array[i] - y_min
        if 0 <= array[i] <= delta:
            output[i] = 2 * array[i]
        elif -1-delta <= array[i] <= 0:
            output[i] = 2 * abs(array[i])
        else:
            output[i] = delta + abs(array[i])

    return output
