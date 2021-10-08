import numpy as np
import bagpy as bp
import pandas as pd
from data import *
import scipy.fftpack
import math
from labellines import labelLines, labelLine

from CurrentDeserailizer import read_log, CurrentData
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

if __name__ == '__main__':

    timecomp = 0

    fig, axs = plt.subplots(len(bags))
    # fig.suptitle('')

    for k in range(0, len(bags)):
        temp = read_log('current/' + logs[k], start_in_zero=False)
        bag = bp.bagreader('bags/' + bags[k])


        print(bag.topic_table)

        # plt.title("Current log chart")
        # plt.xlabel("Time [s]")
        # plt.ylabel("Current [A]")
        # plt.plot(temp.timestamp, temp.currentA)
        # plt.plot(temp.timestamp, temp.currentB)
        # plt.grid()
        # plt.show()


        # moving mean
        N = 137
        filtered = CurrentData()
        filtered.currentA = np.convolve(temp.currentA, np.ones(N)/N, mode='valid')
        filtered.currentB = np.convolve(temp.currentB, np.ones(N)/N, mode='valid')
        filtered.timestamp = temp.timestamp[0:len(temp.timestamp)-N+1]
        # filtered2 = CurrentData()
        # filtered2.currentA = np.convolve(temp2.currentA, np.ones(N)/N, mode='valid')
        # filtered2.currentB = np.convolve(temp2.currentB, np.ones(N)/N, mode='valid')
        # filtered2.timestamp = temp2.timestamp[0:len(temp2.timestamp)-N+1]
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
        # N = len(temp.currentA)
        # # sample spacing
        # diff = np.array(temp.timestamp[1:len(temp.timestamp)])-np.array(temp.timestamp[0:len(temp.timestamp)-1])
        # T = np.mean(diff)
        # print(N, T)
        # x = np.linspace(0.0, N * T, N)
        #
        # yf = scipy.fftpack.fft(temp.currentA)
        # xf = np.linspace(0.0, 1.0 / (2.0 * T), int(float(N) / 2))
        #
        # fig, ax = plt.subplots()
        # ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
        #
        # yf = scipy.fftpack.fft(temp.currentB)
        # xf = np.linspace(0.0, 1.0 / (2.0 * T), int(float(N) / 2))
        #
        # ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
        # plt.show()

        # velmsgs = bag.odometry_data()
        # veldf = pd.read_csv(velmsgs[0])
        # plt.plot(veldf['Time'], veldf['linear.x'])
        # laser = bag.message_by_topic('/robot_driver/laser_ruler/scan_5')
        # laser2 = pd.read_csv(laser)
        # laser2.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
        #
        # plt.plot(laser2['Time'], laser2['range'])
        # plt.show()

        # plt.show()

        velmsgs = bag.odometry_data()
        veldf = pd.read_csv(velmsgs[0])


        timecomp = veldf['Time'][0]

        dx = veldf['pose.x']
        dy = veldf['pose.y']

        dist = dx**2 + dy**2
        dist = np.sqrt(dist)


        # # plt.plot(veldf['Time'], veldf['orientation.z'])
        # plt.plot(veldf['Time'], dist, label='Dist')
        # plt.plot(veldf['Time'], veldf['linear.x'], label='Vel x')
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
        laser4 = bag.message_by_topic('/robot_driver/laser_ruler/scan_3')
        laser4df = pd.read_csv(laser4)
        laser4df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
        #laser2df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
        imu = bag.message_by_topic('/stm_imu')
        imudf = pd.read_csv(imu)

        # plt.plot(imudf['Time'], imudf['linear_acceleration.x'], label='Acc X')
        # plt.plot(imudf['Time'], imudf['linear_acceleration.y'], label='Acc Y')
        # plt.plot(imudf['Time'], imudf['linear_acceleration.z'], label='Acc Z')
        # plt.plot(laser2df['Time']-timecomp, laser2df['ranges_180'], label='lidar 180')
        # plt.plot(laser2df['Time'], laser2df['ranges_180'], label='lidar 180')
        # plt.plot(laserdf['Time'], laserdf['effort_0']+0.58, label='Effort 0')
        # plt.plot(laserdf['Time'], laserdf['effort_1']+0.46, label='Effort 1')
        # # plt.plot(laserdf['Time'], (laserdf['effort_0']+0.58)-(laserdf['effort_1']+0.45))
        # # plt.plot(laserdf['Time'], (laserdf['effort_0']+0.58)+(laserdf['effort_1']+0.45)/veldf['linear.x'])
        # # plt.plot(laserdf['Time'], laserdf['velocity_0']*0.05)
        # # plt.plot(laserdf['Time'], laserdf['velocity_1']*0.05)
        # plt.plot(laser3df['Time'], laser3df['range'], label='scan 1')
        # plt.legend()
        # plt.plot(cmdveldf['Time'], cmdveldf['linear.x'], label='Vel x')
        # plt.show()
        #
        # time = []
        # time2 = []
        # timesum = []
        # coef = []
        # coef2 = []
        # coefsum = []
        # print(len(veldf['Time']), len(laserdf['Time']))
        # j = 0
        # for i in range(0, len(laserdf['velocity_0'])):
        #     if laserdf['Time'][i] > laserdf['Time'][j]:
        #         j += 1
        #         if j >= len(laserdf['Time']) or i >= len(laserdf['Time']):
        #             break
        #         # print(veldf['linear.x'][i], laserdf['effort_0'][j], laserdf['effort_1'][j], i, j)
        #         if (laserdf['velocity_1'][i] > 0.001):
        #             time2.append(laserdf['Time'][i])
        #             coef2.append((laserdf['effort_1'][j]+0.46) / laserdf['velocity_1'][i])
        #             if (laserdf['velocity_0'][i] > 0.001):
        #                 time.append(laserdf['Time'][i])
        #                 coef.append((laserdf['effort_0'][j]+0.58) / laserdf['velocity_0'][i])
        #                 timesum.append(laserdf['Time'][i])
        #                 coefsum.append(coef[-1]+coef2[-1])
        #
        # plt.plot(time-timecomp,  2+np.asarray(coef) / (max(max(coef), abs(min(coef)))), label='Amperopredkosci', color=colours[k+2])
        # plt.plot(time2-timecomp,  np.asarray(coef2) / (max(max(coef2), abs(min(coef2)))), label='Amperopredkosci', color=colours[k+2])
        #
        # plt.plot(timesum - timecomp, -2 + np.asarray(coefsum) / (max(max(coefsum), abs(min(coefsum)))), label='Amperopredkosci', color=colours[k+1])
        # # plt.plot(cmdveldf['Time']-timecomp, cmdveldf['linear.x'], label='Vel x')
        # plt.plot(laserdf['Time']-timecomp, 5+laserdf['velocity_0']*0.05, label='Vel x', color=colours[k+1])
        # plt.plot(laserdf['Time'] - timecomp, 7 + laserdf['velocity_1'] * 0.05, label='Vel x', color=colours[k+1])
        #
        # # liczba 50 wynika ze sredniej maksymalnej liczby - chodzi o to zebysmy mieli odniesienie a nie normalizacje
        # d = np.gradient(laserdf['effort_0'], laserdf['Time'])
        # print(max(d))
        # plt.plot(laserdf['Time']-timecomp, 5+(d/50), label='pochodna', color=colours[k])
        #
        # d = np.gradient(laserdf['effort_1'], laserdf['Time'])
        # print(max(d))
        # plt.plot(laserdf['Time']-timecomp, 7+(d/50), label='pochodna', color=colours[k])
        #
        # d = np.gradient(filtered.currentB, filtered.timestamp)
        # print(max(d))
        # # plt.plot(filtered.timestamp-timecomp, 5+(d/500), label='pochodna', color=colours[k+2])
        # plt.plot(filtered.timestamp-timecomp, 5+(filtered.currentB/2), label='Current A', color=colours[k+2])
        # d = np.gradient(filtered.currentA, filtered.timestamp)
        # print(max(d))
        # # plt.plot(filtered.timestamp-timecomp, 7+(d/500), label='pochodna', color=colours[k+2])
        # plt.plot(filtered.timestamp-timecomp, 7+(filtered.currentA/2), label='Current B', color=colours[k+2])
        # # liczba 200 wynika z sredniej liczby
        # d = np.gradient(laserdf['velocity_0'], laserdf['Time'])
        # print(max(d))
        # plt.plot(laserdf['Time']-timecomp, 5+(d/200), label='pochodna predkosci', color=colours[k+3])
        #
        # d = np.gradient(laserdf['velocity_1'], laserdf['Time'])
        # print(max(d))
        # plt.plot(laserdf['Time']-timecomp, 7+(d/200), label='pochodna predkosci', color=colours[k+3])
        #
        # # plt.plot(veldf['Time']-timecomp, dist, label='Dist')
        # d = np.gradient(dist, veldf['Time']-timecomp)
        # print(max(d))
        # plt.plot(veldf['Time']-timecomp, 3+(d/200), label='pochodna dystansu', color=colours[k+3])
        #
        # d = np.gradient(laser2df['ranges_180'], laser2df['Time'])
        # print(max(d))
        # plt.plot(laser2df['Time']-timecomp, 1+(d*3), label='pochodna dystansu enkoder', color=colours[k+3])
        #
        # #
        # plt.plot(laserdf['Time']-timecomp, laserdf['effort_0']+0.58-5, label='Effort 0',  color=colours[k])
        # plt.plot(laserdf['Time']-timecomp, laserdf['effort_1']+0.46-7, label='Effort 1',  color=colours[k])
        # plt.plot(laser3df['Time']-timecomp,  -3.5+(laser3df['range']*40), label='scan 1', color=colours[k])
        # plt.plot(laser4df['Time']-timecomp,  -3.5+(laser4df['range']*40), label='scan 3', color=colours[k])
        # # plt.plot(laser2df['Time']-timecomp, laser2df['ranges_0'], label='lidar 0')
        # plt.grid()
        # plt.legend()
        # plt.show()

        new_dist = []
        j = 0
        veldf_arr = np.array(veldf['Time'])
        laserdf_arr = np.array(laserdf['Time'])
        # print(len(laserdf_arr), len(veldf_arr))

        new_dist.append(dist[0])
        for i in range(0, len(laserdf['effort_0'])-1):

            while (veldf_arr[j] < laserdf_arr[i]):
                j = j+1
                if j >= len(veldf_arr):
                    break

            if j >= len(veldf_arr):
                if (len(new_dist) < len(laserdf_arr)-1):
                    new_dist.append(dist[j - 2])
                if (len(new_dist) < len(laserdf_arr)):
                    new_dist.append(dist[j-1])

                print(len(new_dist), len(laserdf_arr))
                break
            new_dist.append(dist[j])
            # print(i, j)

        # new_dist.append(dist[len(dist)-1])
        dist_coef = new_dist[0]

        axs[k].plot(new_dist-dist_coef, laserdf['effort_0']+0.58, label='Effort 0 ',  color=colours[1])
        axs[k].plot(new_dist-dist_coef, laserdf['effort_1']+0.46, label='Effort 1 ',  color=colours[2])
        axs[k].plot(new_dist-dist_coef, laserdf['velocity_0']/35, label='Velocity 0 ',  color=colours[3])
        axs[k].plot(new_dist-dist_coef, laserdf['velocity_1']/35, label='Velocity 1 ',  color=colours[4])
        # axs[k].set_xlim(-0.5, 2.10)

        # plt.plot(new_dist,  -3.5+(laser3df['range']*40), label='scan 1', color=colours[k])
        # plt.plot(new_dist,  -3.5+(laser4df['range']*40), label='scan 3', color=colours[k])
        # plt.plot(laser2df['Time']-timecomp, laser2df['ranges_0'], label='lidar 0')
        axs[k].grid()
        if (k == round(len(bags)/2)):
            axs[k].set_ylabel("Current [A] / Velocity [rad/s]/35")

        if (k == 0):
            axs[k].legend()

    #
    plt.xlabel("Distance [m]")

    plt.show()
