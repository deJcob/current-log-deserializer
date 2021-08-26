import numpy as np
import bagpy as bp
import pandas as pd
import scipy.fftpack
import math

from CurrentDeserailizer import read_log, CurrentData
from matplotlib import pyplot as plt

if __name__ == '__main__':
    temp = read_log('current/current log 23-07-2021 16-03-38', start_in_zero=False)
    bag = bp.bagreader('bags/2021-07-23-16-03-37.bag')


    print(bag.topic_table)

    plt.title("Current log chart")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.plot(temp.timestamp, temp.currentA)
    plt.plot(temp.timestamp, temp.currentB)
    plt.grid()
    plt.show()


    # moving mean
    # N = 20
    # filtered = CurrentData()
    # filtered.currentA = np.convolve(temp.currentA, np.ones(N)/N, mode='valid')
    # filtered.currentB = np.convolve(temp.currentB, np.ones(N)/N, mode='valid')
    # filtered.timestamp = temp.timestamp[0:len(temp.timestamp)-N+1]
    # # filtered2 = CurrentData()
    # # filtered2.currentA = np.convolve(temp2.currentA, np.ones(N)/N, mode='valid')
    # # filtered2.currentB = np.convolve(temp2.currentB, np.ones(N)/N, mode='valid')
    # # filtered2.timestamp = temp2.timestamp[0:len(temp2.timestamp)-N+1]
    # plt.title("Current log chart filtered")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Current [A]")
    # plt.grid()
    # # plt.plot(temp.timestamp, temp.currentA)
    # # plt.plot(temp.timestamp, temp.currentB)
    # plt.plot(filtered.timestamp-filtered.timestamp[0], filtered.currentA+0.14)
    # plt.plot(filtered.timestamp-filtered.timestamp[0], filtered.currentB)
    # plt.plot(filtered2.timestamp-filtered2.timestamp[0], filtered2.currentA+2.14)
    # plt.plot(filtered2.timestamp-filtered2.timestamp[0], filtered2.currentB+2)
    # plt.plot(temp.timestamp, temp.currentB)

    # FFT
    N = len(temp.currentA)
    # sample spacing
    diff = np.array(temp.timestamp[1:len(temp.timestamp)])-np.array(temp.timestamp[0:len(temp.timestamp)-1])
    T = np.mean(diff)
    print(N, T)
    x = np.linspace(0.0, N * T, N)

    yf = scipy.fftpack.fft(temp.currentA)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), int(float(N) / 2))

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))

    yf = scipy.fftpack.fft(temp.currentB)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), int(float(N) / 2))

    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.show()

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

    velmsgs = bag.odometry_data()
    veldf = pd.read_csv(velmsgs[0])

    dx = veldf['pose.x']
    dy = veldf['pose.y']

    dist = dx**2 + dy**2
    dist = np.sqrt(dist)

    # plt.plot(veldf['Time'], veldf['orientation.z'])
    plt.plot(veldf['Time'], dist)
    plt.plot(veldf['Time'], veldf['linear.x'])
    # plt.plot(veldf['Time'], )
    laser = bag.message_by_topic('/joint_states/')
    laserdf = pd.read_csv(laser)
    cmdvel = bag.message_by_topic('/diff_drive/cmd_vel')
    cmdveldf = pd.read_csv(cmdvel)
    laser2 = bag.message_by_topic('/scan')
    laser2df = pd.read_csv(laser2)
    laser3 = bag.message_by_topic('/robot_driver/laser_ruler/scan_1')
    laser3df = pd.read_csv(laser3)
    laser3df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
    # laser2df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
    imu = bag.message_by_topic('/stm_imu')
    imudf = pd.read_csv(imu)

    plt.plot(imudf['Time'], imudf['linear_acceleration.x'])
    plt.plot(imudf['Time'], imudf['linear_acceleration.y'])
    plt.plot(imudf['Time'], imudf['linear_acceleration.z'])
    plt.plot(laser2df['Time'], laser2df['ranges_0'])
    plt.plot(laser2df['Time'], laser2df['ranges_180'])
    plt.plot(laserdf['Time'], laserdf['effort_0']+0.58)
    plt.plot(laserdf['Time'], laserdf['effort_1']+0.46)
    # plt.plot(laserdf['Time'], (laserdf['effort_0']+0.58)-(laserdf['effort_1']+0.45))
    # plt.plot(laserdf['Time'], (laserdf['effort_0']+0.58)+(laserdf['effort_1']+0.45)/veldf['linear.x'])
    # plt.plot(laserdf['Time'], laserdf['velocity_0']*0.05)
    # plt.plot(laserdf['Time'], laserdf['velocity_1']*0.05)
    plt.plot(laser3df['Time'], laser3df['range'])

    plt.plot(cmdveldf['Time'], cmdveldf['linear.x'])
    plt.show()


