from CurrentDeserailizer import read_log
from matplotlib import pyplot as plt

if __name__ == '__main__':
    temp = read_log('test_file')

    plt.title("Current log chart")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.plot(temp.timestamp, temp.currentA)
    plt.plot(temp.timestamp, temp.currentB)
    plt.show()