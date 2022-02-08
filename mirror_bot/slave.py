import time
import socket                                         
import numpy as np
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig1
from dynamic_graph_head import SimHead, ThreadHead
from bullet_utils.env import BulletEnv
from robot_properties_nyu_finger.wrapper import NYUFingerRobot

mode = 'hardware'  # hardware / env


def start_hw_thread():
    if mode == 'hardware':
        head = dynamic_graph_manager_cpp_bindings.DGMHead(
            NYUFingerDoubleConfig1.dgm_yaml_path)
    else:
        env = BulletEnv()
        config = NYUFingerDoubleConfig1()
        finger = NYUFingerRobot(config=config)
        head = SimHead(finger, with_sliders=False)
        env.add_robot(finger)
    
    hold_ctrl = HoldPDController(head, 3., 0.05, False)

    if mode == 'hardware':
        thread_head = ThreadHead(
            0.001,  # dt.
            [hold_ctrl],  # Safety controllers.
            {'head': head},  # Heads to read / write from.
            [],
        )
    else:
        thread_head = ThreadHead(
            0.001,  # dt.
            [hold_ctrl],  # Safety controllers.
            {'head': head},  # Heads to read / write from.
            [],
            env
        )
    thread_head.start()

    return head


if __name__ == "__main__":

    # start socket thread
    # start main program
    head = start_hw_thread()

    target_pos = np.array([0., 0., 0. ])
    target_vel = np.array([0., 0., 0. ])


    P = 3 * np.ones(3)
    D = 0.2 * np.ones(3)
    dt = 0.001
    next_time = time.time() + dt


    # TODO: Use Thread
    while (True):
        if time.time() >= next_time:
            next_time += dt

            ###
            # Get the latest measurements from the shared memory.
            head.read()

            ###
            # Set the P and D gains.
            head.set_control('ctrl_joint_position_gains', P)
            head.set_control('ctrl_joint_velocity_gains', D)

            ###
            # Set PD target position and velocity.
            head.set_control('ctrl_joint_positions', target_pos)
            head.set_control('ctrl_joint_velocities', target_vel)

            ###
            # Write the results into shared memory again.
            head.write()

        time.sleep(0.0001)
    # while True:
    #     joint_positions = robot_head.get_sensor("joint_positions")
    #     joint_velocities = robot_head.get_sensor("joint_velocities")
    #     print(joint_positions, joint_velocities)
    #     time.sleep(0.001)
