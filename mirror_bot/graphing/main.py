import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

class grapher:
    def __init__(self):
        self.leader_pos = [[],[],[]]
        self.leader_vel = [[],[],[]]
        self.follower_pos = [[],[],[]]
        self.follower_vel = [[],[],[]]
        self.count = 0
        self.fig = self.init_plot()
        return
    
    def get_plot(self):
        return self.fig

    def init_plot(self):
        fig = plt.figure(figsize=(12,18), facecolor='#DEDEDE')
        
        pos_plot1 = plt.subplot(321)
        pos_plot1.set_title('Position')
        pos_plot2 = plt.subplot(323)
        pos_plot3 = plt.subplot(325)

        pos_plots = [pos_plot1, pos_plot2, pos_plot3]
        for plot in pos_plots:
            plot.set_facecolor('#DEDEDE')

        vel_plot1 = plt.subplot(322)
        vel_plot1.set_title('Velocity')
        vel_plot2 = plt.subplot(324)
        vel_plot3 = plt.subplot(326)

        vel_plots = [vel_plot1, vel_plot2, vel_plot3]
        for plot in vel_plots:
            plot.set_facecolor('#DEDEDE')

        self.pos_plots = pos_plots
        self.vel_plots = vel_plots
        return fig

    def step(self, head1, head2):
        for i in range(3):
            self.leader_pos[i].append(head1.get('pos')[i])
            self.leader_vel[i].append(head1.get('vel')[i])
            self.follower_pos[i].append(head2.get('pos')[i])
            self.follower_vel[i].append(head2.get('vel')[i])
        self.count += 1
        self.plot()
        return
    
    def plot(self):
        if self.count > 10*1000:
            self.leader_pos.popleft()
            self.leader_vel.popleft()
            self.follower_pos.popleft()
            self.follower_vel.popleft()

        pos_plots = self.pos_plots
        vel_plots = self.vel_plots

        for i in range(len(pos_plots)):
            pos_plots[i].cla()

            data = self.leader_pos[i]
            pos_plots[i].plot(data)
            pos_plots[i].scatter(len(data)-1, data[-1])
            pos_plots[i].text(len(data)-1, data[-1]+2, data[-1])
            
            data = self.follower_pos[i]
            pos_plots[i].plot(data)
            pos_plots[i].scatter(len(data)-1, data[-1])
            pos_plots[i].text(len(data)-1, data[-1]+2, data[-1])
            
            # pos_plots[i].set_xlim(0,10*1000)
        
        for i in range(len(vel_plots)):
            vel_plots[i].cla()

            data = self.leader_vel[i]
            vel_plots[i].plot(data)
            vel_plots[i].scatter(len(data)-1, data[-1])
            vel_plots[i].text(len(data)-1, data[-1]+2, data[-1])
            
            data = self.follower_vel[i]
            vel_plots[i].plot(data)
            vel_plots[i].scatter(len(data)-1, data[-1])
            vel_plots[i].text(len(data)-1, data[-1]+2, data[-1])
            
            # vel_plots[i].set_xlim(0,10*1000)

        return


def rand_3():
    x = np.random.rand(1, 3)
    x = list(x[0])
    return x

def step_plot(_,grapher):
    # get data
    head1 = {'pos':rand_3(),'vel':rand_3()}
    head2 = {'pos':rand_3(),'vel':rand_3()}
    grapher.step(head1, head2)
    return


test = grapher()
fig = test.get_plot()

# ani = FuncAnimation(fig, step_plot, fargs=[test], interval=1)
# plt.show()
a = time.time()
for i in range(1000):
    print(i)
    _ = 1
    step_plot(_,test)
b = time.time()
print(b-a)
plt.show()
