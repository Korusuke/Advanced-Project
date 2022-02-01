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