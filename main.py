# This is a sample Python script.
import copy

import numpy as np
from matplotlib import pyplot as plt

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class currentData:

    def __init__(self):
        self.timestamp = []
        self.currentA = []
        self.currentB = []


def readLog(name, startInZero = True):

    data = currentData()

    with open(name, "rb") as f:

        byte = f.read(8)
        timestamp_1 = np.frombuffer(byte, dtype='int64')[0]/(10**9)

        if startInZero:
            data.timestamp.append(0)
        else:
            data.timestamp.append(timestamp_1)

        while byte != b"":
            byte = f.read(4)
            size = np.frombuffer(byte, dtype='int32')[0]
            byte = f.read(4)
            for i in range(size):
                data.currentA.append(np.frombuffer(f.read(8), dtype='float64')[0])
                data.currentB.append(np.frombuffer(f.read(8), dtype='float64')[0])

            byte = f.read(8)
            if byte == b"":
                for i in range(size):
                    data.timestamp.append(data.timestamp[-1] + time_delta)
                data.timestamp.pop(-1)
                break
            timestamp_2 = np.frombuffer(byte, dtype='int64')[0]/(10**9)
            time_delta = (timestamp_2 - timestamp_1) / size

            for i in range(size):
                data.timestamp.append(data.timestamp[-1] + time_delta)
            timestamp_1 = timestamp_2

    return data

# hexdump -C current\ log\ 23-07-2021\ 14-09-04 -n 5000

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    temp = readLog('test_file')

    plt.title("Current log chart")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.plot(temp.timestamp, temp.currentA)
    plt.plot(temp.timestamp, temp.currentB)
    plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
