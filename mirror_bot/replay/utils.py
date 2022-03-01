import argparse
from turtle import position
import numpy as np
import pinocchio as pin


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', type=str,
                        choices=['record', 'play'])
    parser.add_argument('robot', type=int, choices=[1, 2])
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    return args


class RecorderController:
    def __init__(self, head, pin_robot, fileName):
        """
        Args:
            head: Instance of DGHead or SimHead.
        """
        self.head = head

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        self.fileName = fileName
        self.file = None

        self.zeros_pos = np.zeros_like(self.joint_positions)
        self.robot = pin_robot

    def closeFile(self):
        self.file.close()
        return

    def warmup(self, thread_head):
        self.base_pos = self.joint_positions.copy()
        self.file = open(self.fileName, "w")
        self.file.write(f"{self.joint_positions}---{self.joint_velocities}\n")
        return

    def rnea(self, q, dq, ddq):
        return pin.rnea(self.robot.model, self.robot.data, q, dq, ddq)

    def run(self, thread_head):
        self.tau = self.rnea(self.joint_positions,
                             self.zeros_pos, self.zeros_pos)
        self.head.set_control("ctrl_joint_torques", self.tau)
        self.file.write(f"{self.joint_positions}---{self.joint_velocities}\n")
        return


class PlayBackController:
    def __init__(self, head, pin_robot, fileName):
        """
        Args:
            head: Instance of DGHead or SimHead.
            leader_head: Instance of DGHead or SimHead
        """
        self.head = head

        self.des_position = None
        self.des_velocity = None

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        self.fileName = fileName
        self.file = None

        self.zeros_pos = np.zeros_like(self.joint_positions)
        self.robot = pin_robot

    def closeFile(self):
        self.file.close()
        return

    def read(self):
        position, velocity = self.file.readline().strip().split('---')
        self.des_position = np.fromstring(position[1:-1], dtype=float, sep=' ')
        self.des_velocity = np.fromstring(velocity[1:-1], dtype=float, sep=' ')
        return

    def warmup(self, thread_head):
        self.file = open(self.fileName, "r")
        self.read()
        return

    def rnea(self, q, dq, ddq):
        return pin.rnea(self.robot.model, self.robot.data, q, dq, ddq)

    def run(self, thread_head):
        self.read()

        P = 3 * np.ones(3)
        D = 0.05 * np.ones(3)

        self.tau = (
            P * (self.des_position - self.joint_positions)
            + D * (self.des_velocity - self.joint_velocities)
        )
        self.tau += self.rnea(self.des_position,
                              self.zeros_pos, self.zeros_pos)
        self.head.set_control("ctrl_joint_torques", self.tau)
        return
