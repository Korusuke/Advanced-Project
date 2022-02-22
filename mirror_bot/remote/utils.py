import numpy as np
import pinocchio as pin


class GravityCompensationController:
    def __init__(self, head, pin_robot, shared_vars):
        """
        Args:
            head: Instance of DGHead or SimHead.
        """
        self.head = head

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")
        self.shared_vars = shared_vars
        shared_vars['leader_pos'] = self.joint_positions
        shared_vars['leader_vel'] = self.joint_velocities

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
    def __init__(self, head, shared_vars):
        """
        Args:
            head: Instance of DGHead or SimHead.
            leader_head: Instance of DGHead or SimHead
        """
        self.head = head
        self.shared_vars = shared_vars

        self.des_position = shared_vars.get("leader_pos")
        self.des_velocity = shared_vars.get("leader_vel")

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        shared_vars['follower_pos'] = self.joint_positions
        shared_vars['follower_vel'] = self.joint_velocities

    def warmup(self, thread_head):
        P = 3 * np.ones(3)
        D = 0.05 * np.ones(3)
        self.head.set_control('ctrl_joint_position_gains', P)
        self.head.set_control('ctrl_joint_velocity_gains', D)
        return

    def run(self, thread_head):
        self.des_position = np.array(self.shared_vars.get("leader_pos"))
        self.des_velocity = np.array(self.shared_vars.get("leader_vel"))

        self.head.set_control("ctrl_joint_positions", self.des_position)
        self.head.set_control("ctrl_joint_velocities", self.des_velocity)
        return


class MirrorHeadController:
    def __init__(self, head, shared_vars):
        """
        Args:
            head: Instance of DGHead or SimHead.
            leader_head: Instance of DGHead or SimHead
        """
        self.head = head
        self.shared_vars = shared_vars

        self.des_position = shared_vars.get("leader_pos")
        self.des_velocity = shared_vars.get("leader_vel")

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        shared_vars['follower_pos'] = self.joint_positions
        shared_vars['follower_vel'] = self.joint_velocities

    def warmup(self, thread_head):

        return

    def run(self, thread_head):
        P = 3 * np.ones(3)
        D = 0.05 * np.ones(3)

        self.des_position = self.shared_vars.get("leader_pos")
        self.des_velocity = self.shared_vars.get("leader_vel")

        self.tau = (
            P * (self.des_position - self.joint_positions)
            + D * (self.des_velocity - self.joint_velocities)
        )
        self.head.set_control("ctrl_joint_torques", self.tau)
        return
