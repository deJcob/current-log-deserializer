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
        bag = bp.bagreader('bags/' + bags[k])

        print(bag.topic_table)

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

        dx = np.array(veldf['pose.x'])
        dy = np.array(veldf['pose.y'])

        # if (min(dx) < 0):                   # Shifting data to be in the first quadrant of the coordinate system for easier distance calculation
        #     dx = dx + abs(min(dx))
        # else:
        #     dx = dx - min(dx)
        #
        # if (min(dy) < 0):
        #     dy = dy + abs(min(dy))
        # else:
        #     dy = dy - min(dy)

        print(dx[0], dy[0])

        # dist = dx**2 + dy**2
        dist = [0]
        for i in range(0, len(dx)-1):
            dd = math.sqrt((dx[i+1]-dx[i])**2+(dy[i+1]-dy[i])**2)
            dist.append(dist[-1]+dd)

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

        # plt.plot(laserdf['Time']-timecomp, laserdf['effort_0']+0.58-5, label='Effort 0',  color=colours[k])
        # plt.plot(laserdf['Time']-timecomp, laserdf['effort_1']+0.46-7, label='Effort 1',  color=colours[k])
        # plt.plot(laser3df['Time']-timecomp,  -3.5+(laser3df['range']*40), label='scan 1', color=colours[k])
        # plt.plot(laser4df['Time']-timecomp,  -3.5+(laser4df['range']*40), label='scan 3', color=colours[k])
        # # plt.plot(laser2df['Time']-timecomp, laser2df['ranges_0'], label='lidar 0')
        # plt.grid()
        # plt.legend()
        # plt.show()


        eff0 = np.array(laserdf['effort_0'] + 0.58)
        eff1 = np.array(laserdf['effort_1'] + 0.46)
        tim = np.array(laserdf['Time'] - timecomp)
        vel0 = np.array(laserdf['velocity_0'])
        vel1 = np.array(laserdf['velocity_1'])

        axs[k].plot(laserdf['Time']-timecomp, laserdf['effort_0']+0.58, label='Średni prąd, silnik 0',  color=colours[1])
        axs[k].plot(laserdf['Time']-timecomp, laserdf['effort_1']+0.46, label='Średni prąd, silnik 1',  color=colours[2])
        axs[k].plot(laserdf['Time']-timecomp, laserdf['velocity_0']/10, label='Prędkość, silnik 0',  color=colours[3])
        axs[k].plot(laserdf['Time']-timecomp, laserdf['velocity_1']/10, label='Prędkość, silnik 1',  color=colours[4])

        max_x = max(max_x, max(tim))

        # plt.plot(new_dist,  -3.5+(laser3df['range']*40), label='scan 1', color=colours[k])
        # plt.plot(new_dist,  -3.5+(laser4df['range']*40), label='scan 3', color=colours[k])
        # plt.plot(laser2df['Time']-timecomp, laser2df['ranges_0'], label='lidar 0')
        axs[k].grid()
        if (k == round(len(bags)/2)):
            axs[k].set_ylabel("prąd [A] / prędkość obrotowa [rad/s]/10", fontsize=16)

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

    # plt.show()

    fig.savefig('current time' + collection_name.replace("/", "").replace(".", "") + '.png')
