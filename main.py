import numpy as np
import bagpy as bp
import pandas as pd

from CurrentDeserailizer import read_log, CurrentData
from matplotlib import pyplot as plt

if __name__ == '__main__':
    temp = read_log('current log 23-07-2021 16-07-02', start_in_zero=False)
    temp2 = read_log('current log 23-07-2021 14-09-04', start_in_zero=False)
    bag = bp.bagreader('2021-07-23-16-07-01.bag')
    print(bag.topic_table)

    # plt.title("Current log chart")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Current [A]")
    # plt.plot(temp.timestamp, temp.currentA)
    # plt.plot(temp.timestamp, temp.currentB)
    # plt.grid()
    # plt.show()


    # moving mean
    N = 300
    filtered = CurrentData()
    filtered.currentA = np.convolve(temp.currentA, np.ones(N)/N, mode='valid')
    filtered.currentB = np.convolve(temp.currentB, np.ones(N)/N, mode='valid')
    filtered.timestamp = temp.timestamp[0:len(temp.timestamp)-N+1]
    filtered2 = CurrentData()
    filtered2.currentA = np.convolve(temp2.currentA, np.ones(N)/N, mode='valid')
    filtered2.currentB = np.convolve(temp2.currentB, np.ones(N)/N, mode='valid')
    filtered2.timestamp = temp2.timestamp[0:len(temp2.timestamp)-N+1]
    plt.title("Current log chart filtered")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.grid()
    # plt.plot(temp.timestamp, temp.currentA)
    # plt.plot(temp.timestamp, temp.currentB)
    plt.plot(filtered.timestamp-filtered.timestamp[0], filtered.currentA+0.14)
    plt.plot(filtered.timestamp-filtered.timestamp[0], filtered.currentB)
    plt.plot(filtered2.timestamp-filtered2.timestamp[0], filtered2.currentA+2.14)
    plt.plot(filtered2.timestamp-filtered2.timestamp[0], filtered2.currentB+2)
    # plt.plot(temp.timestamp, temp.currentB)

    # velmsgs = bag.odometry_data()
    # veldf = pd.read_csv(velmsgs[0])
    # plt.plot(veldf['Time'], veldf['linear.x'])
    # laser = bag.message_by_topic('/robot_driver/laser_ruler/scan_5')
    # laser2 = pd.read_csv(laser)
    # laser2.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
    #
    # plt.plot(laser2['Time'], laser2['range'])
    # plt.show()

    plt.show()

