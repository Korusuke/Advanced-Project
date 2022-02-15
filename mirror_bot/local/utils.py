import numpy as np
import pinocchio as pin


class GravityCompensationController:
    def __init__(self, head, pin_robot):
        """
        Args:
            head: Instance of DGHead or SimHead.
        """
        self.head = head

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        self.zeros_pos = np.zeros_like(self.joint_positions)
        self.robot = pin_robot

    def warmup(self, thread_head):
        self.base_pos = self.joint_positions.copy()
        return

    def rnea(self, q, dq, ddq):
        return pin.rnea(self.robot.model, self.robot.data, q, dq, ddq)

    def run(self, thread_head):
        self.tau = self.rnea(self.joint_positions,
                             self.zeros_pos, self.zeros_pos)
        # print(self.tau)
        self.head.set_control("ctrl_joint_torques", self.tau)
        return


class MirrorVelocityPositionHWController:
    def __init__(self, head, leader_head):
        """
        Args:
            head: Instance of DGHead or SimHead.
            leader_head: Instance of DGHead or SimHead
        """
        self.head = head
        self.leader_head = leader_head

        self.des_position = leader_head.get_sensor("joint_positions")
        self.des_velocity = leader_head.get_sensor("joint_velocities")

    def warmup(self, thread_head):
        P = np.ones(3)
        D = np.ones(3)
        self.head.set_control('ctrl_joint_position_gains', P)
        self.head.set_control('ctrl_joint_velocity_gains', D)
        return

    def run(self, thread_head):
        self.head.set_control("ctrl_joint_positions", self.des_position)
        self.head.set_control("ctrl_joint_velocities", self.des_velocity)
        return
