import numpy as np
import bagpy as bp
import pandas as pd
from data_prec import *
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
    max_x = 0
    min_x = 100000

    for k in range(0, len(bags)):
        bag = bp.bagreader('prec/' + bags[k])

        # print(bag.topic_table)

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

        laser2 = bag.message_by_topic('/robot_driver/laser_ruler/scan_0')
        laser6df = pd.read_csv(laser2)
        laser6df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
        laser3 = bag.message_by_topic('/robot_driver/laser_ruler/scan_1')
        laser3df = pd.read_csv(laser3)
        laser3df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
        laser4 = bag.message_by_topic('/robot_driver/laser_ruler/scan_2')
        laser4df = pd.read_csv(laser4)
        laser4df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")
        laser5 = bag.message_by_topic('/robot_driver/laser_ruler/scan_3')
        laser5df = pd.read_csv(laser5)
        laser5df.replace([np.inf, -np.inf], 10.0).dropna(subset=["range"], how="all")

        imu = bag.message_by_topic('/stm_imu')
        imudf = pd.read_csv(imu)

        tim = np.array(veldf['Time'] - timecomp)
        vel0 = np.array(veldf['linear.x'])

        min_tmp = 0.0
        max_tmp = 0.0
        for j in range(0, len(tim)):
            if vel0[j] > 0.015:
                min_tmp = tim[j-15]
                print(min_tmp)
                break

        min_x = min(min_x, min_tmp)

        for j, e in reversed(list(enumerate(vel0))):
            if vel0[j] > 0.015:
                max_tmp = tim[j + 15]-min_tmp
                print(max_tmp)
                break

        max_x = max(max_x, max_tmp)

        axs[k].plot(veldf['Time'] - timecomp-min_tmp, veldf['linear.x'], label='Prędkość liniowa', color=colours[1])

        axs[k].plot(laser2df['Time']-timecomp-min_tmp, laser2df['ranges_1'], label='Lidar 1', color=colours[2])
        axs[k].plot(laser2df['Time']-timecomp-min_tmp, laser2df['ranges_0'], label='Lidar 0', color=colours[3])
        axs[k].plot(laser2df['Time']-timecomp-min_tmp, laser2df['ranges_359'], label='Lidar -1', color=colours[4])
        axs[k].plot(laser6df['Time']-timecomp-min_tmp,  laser6df['range']*10, label='Linijka 0', color=colours[5])
        axs[k].plot(laser3df['Time']-timecomp-min_tmp,  laser3df['range']*10, label='Linijka 1', color=colours[6])
        axs[k].plot(laser4df['Time']-timecomp-min_tmp,  laser4df['range']*10, label='Linijka 2', color=colours[7])
        axs[k].plot(laser5df['Time']-timecomp-min_tmp,  laser5df['range']*10, label='Linijka 3', color=colours[8])


        axs[k].grid()

        if (k == round(len(bags)/2)):
            axs[k].set_ylabel("Prędkość [m/s] / Odległość [m]", fontsize=16)

        if (k == 0):
            axs[k].legend(loc=1)
    #

    for k in range(0, len(bags)):
        axs[k].set_xlim(0.0, max_x)

    plt.xlabel("Czas [s]", fontsize=16)
    fig.suptitle(collection_name, fontsize=16)
    fig.set_size_inches(12, 18)
    fig.subplots_adjust(
        top=0.95,
        bottom=0.049,
        left=0.07,
        right=0.97,
        hspace=0.2,
        wspace=0.2
    )

    plt.show()

    fig.savefig('prec ster' + collection_name.replace("/", "").replace(".", "") + '.png')