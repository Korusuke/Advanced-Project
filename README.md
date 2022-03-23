# Advanced-Project

## Setup-Guide

Install treep and clone all required repos using treep

```bash
python3 -m pip install -U treep
git clone https://github.com/machines-in-motion/treep_machines_in_motion
treep --clone NYU_FINGER
```

Once you have the workspace folder you can build it using the following

```bash
source /opt/openrobots/setup.bash
source /opt/ros/foxy/setup.bash

colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release -DPYBIND11_TEST=OFF -DBUILD_TESTING=OFF

source ~/Desktop/advanced/workspace/install/setup.bash

colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release -DPYBIND11_TEST=OFF -DBUILD_TESTING=OFF
```

## Different versions

### mirror_bot/local (deprecated)

Uses gravity compensation in only the leader bot and PD controller in the follower. Both bots needs to be connected to the same host. Also has the HW direct controller which directly sets the position and velocity using the Hardware, intead of calculating the tau.

### mirror_bot/localv2

Uses gravity compensation in both the bots and and extra PD controller in the follower. Both bots needs to be connected to the same host. Using gravity compensation in the follower bot resulted in more precise control, it was not apparent at first due to the error being small, but the error can be measured accross controllers by logging the diff in leader and follower position over time.  


### mirror_bot/remote

Its same as the localv2 but can be used accross network and bots can be connected to different hosts. Uses sockets for communication. The performance drop from local to local network is negligible, further testing required for different network speeds and packet loss. 

### mirror_bot/replay

Just a simple script to record motion on any bot and replay the same motion using the log file.

### mirror_bot/feedback

Force feedback from the follower bot so that the controller can feel if something is blocking the path of the follower. One issue currently is that there is a spring action in the leader which leads to a positive feedback loop if the leader is tensioned and then released. Not sure how can this be solved, since there are no force sensors to work with. 

In all the leader uses, a P controller in addition to the gravity compensation we had in previous experiments. The follower is same as previous, a PD controller + gravity compensation.

