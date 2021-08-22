import numpy as np


class CurrentData:

    def __init__(self):
        self.timestamp = []
        self.currentA = []
        self.currentB = []


def read_log(name, start_in_zero = True):

    data = CurrentData()

    with open(name, "rb") as f:

        byte = f.read(8)                                            # Timepstamp is uint64_t
        timestamp_1 = np.frombuffer(byte, dtype='int64')[0]/(10**9) # nsec to sec

        if start_in_zero:                       # True if you want to normalize time from 0
            data.timestamp.append(np.float64(0.0))
        else:                                   # Time from ros.time.now().ToNsec
            data.timestamp.append(timestamp_1)

        while byte != b"":
            byte = f.read(4)
            size = np.frombuffer(byte, dtype='int32')[0] # size is size_t type
            f.read(4)                                    # always zeros
            for i in range(size):
                data.currentA.append(np.frombuffer(f.read(8), dtype='float64')[0])
                data.currentB.append(np.frombuffer(f.read(8), dtype='float64')[0])

            byte = f.read(8)
            if byte == b"":    # if there is no next timestamp there is no more data
                for i in range(size):
                    data.timestamp.append(data.timestamp[-1] + time_delta)
                data.timestamp.pop(-1)                       # last element should be removed
                break
            timestamp_2 = np.frombuffer(byte, dtype='int64')[0]/(10**9)
            time_delta = (timestamp_2 - timestamp_1) / size

            for i in range(size):
                data.timestamp.append(data.timestamp[-1] + time_delta)
            timestamp_1 = timestamp_2

    return data

