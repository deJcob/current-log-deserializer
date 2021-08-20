import numpy as np

from CurrentDeserailizer import read_log, CurrentData
from matplotlib import pyplot as plt

if __name__ == '__main__':
    temp = read_log('test_file')

    # plt.title("Current log chart")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Current [A]")
    # plt.plot(temp.timestamp, temp.currentA)
    # plt.plot(temp.timestamp, temp.currentB)
    # plt.grid()
    # plt.show()

    # moving mean
    N = 140
    filtered = CurrentData()
    filtered.currentA = np.convolve(temp.currentA, np.ones(N)/N, mode='valid')
    filtered.currentB = np.convolve(temp.currentB, np.ones(N)/N, mode='valid')
    filtered.timestamp = temp.timestamp[0:len(temp.timestamp)-N+1]
    plt.title("Current log chart filtered")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.grid()
    plt.plot(temp.timestamp, temp.currentA)
    plt.plot(temp.timestamp, temp.currentB)
    plt.plot(filtered.timestamp, filtered.currentA)
    plt.plot(filtered.timestamp, filtered.currentB)
    # plt.plot(temp.timestamp, temp.currentB)
    plt.show()

