# This is a sample Python script.
import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# hexdump -C current\ log\ 23-07-2021\ 14-09-04 -n 5000

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("test_file", "rb") as f:
        byte = f.read(8)
        timestamp = np.frombuffer(byte, dtype='int64')
        print(timestamp)
        byte = f.read(4)
        size = np.frombuffer(byte, dtype='int32')
        byte = f.read(4)
        print(size[0])
        for i in range(size[0]):
            byte1 = f.read(8)
            byte2 = f.read(8)
            print(np.frombuffer(byte1, dtype='float64'), np.frombuffer(byte2, dtype='float64'))

        while byte != b"":
            # print(byte)
            # Do stuff with byte.
            byte = f.read(8)
            timestamp = np.frombuffer(byte, dtype='int64')
            # print(timestamp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
