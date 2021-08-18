# This is a sample Python script.
import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class currentLog:

    def __init__(self):
        self.timestamps = []
        self.currentA = []
        self.currentB = []


def readLog(name):

    data = currentLog()
    frames_counter = 0

    with open(name, "rb") as f:
        byte = bytes(1)
        while byte != b"":
            frames_counter += 1
            byte = f.read(8)
            timestamp = np.frombuffer(byte, dtype='int64')[0]
            print(timestamp)
            byte = f.read(4)
            size = np.frombuffer(byte, dtype='int32')[0]
            byte = f.read(4)
            print(size)
            for i in range(size):
                data.currentA.append(np.frombuffer(f.read(8), dtype='float64')[0])
                data.currentB.append(np.frombuffer(f.read(8), dtype='float64')[0])
            print(frames_counter)

        while byte != b"":
            # print(byte)
            # Do stuff with byte.
            byte = f.read(8)
            timestamp = np.frombuffer(byte, dtype='int64')
            # print(timestamp)

    return data

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# hexdump -C current\ log\ 23-07-2021\ 14-09-04 -n 5000

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readLog('test_file')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
