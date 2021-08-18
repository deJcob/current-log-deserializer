import numpy as np


class CurrentData:

    def __init__(self):
        self.timestamp = []
        self.currentA = []
        self.currentB = []


def read_log(name, start_in_zero = True):

    data = CurrentData()

    with open(name, "rb") as f:

        byte = f.read(8)
        timestamp_1 = np.frombuffer(byte, dtype='int64')[0]/(10**9)

        if start_in_zero:
            data.timestamp.append(0)
        else:
            data.timestamp.append(timestamp_1)

        while byte != b"":
            byte = f.read(4)
            size = np.frombuffer(byte, dtype='int32')[0]
            f.read(4)
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

