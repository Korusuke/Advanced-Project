import numpy as np
import pinocchio as pin


class GravityCompensationControllerWithFeedback:
    def __init__(self, head, pin_robot, shared_vars):
        """
        Args:
            head: Instance of DGHead or SimHead
            pin_robot: Pinocchio robot instance
            shared_vars: Dictonary containing all the shared variables
        """
        self.head = head
        self.shared_vars = shared_vars
        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        shared_vars['leader_pos'] = self.joint_positions
        shared_vars['leader_vel'] = self.joint_velocities

        self.follower_pos = shared_vars['follower_pos']

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
        # EXPERIMENTAL
        diff = self.shared_vars['follower_pos'] - \
            self.shared_vars['leader_pos']
        P = 1 * np.ones(3)

        self.tau += (
            P * diff
        )
        # END OF EXPERIMENTAL

        self.head.set_control("ctrl_joint_torques", self.tau)
        return


class MirrorHeadGravityControllerForceFeedback:
    def __init__(self, head, pin_robot, shared_vars):
        """
        Args:
            head: Instance of DGHead or SimHead
            pin_robot: Pinocchio robot instance
            shared_vars: Dictonary containing all the shared variables
        """
        self.head = head
        self.shared_vars = shared_vars

        self.joint_positions = head.get_sensor("joint_positions")
        self.joint_velocities = head.get_sensor("joint_velocities")

        shared_vars['follower_pos'] = self.joint_positions
        shared_vars['follower_vel'] = self.joint_velocities

        self.zeros_pos = np.zeros_like(self.joint_positions)
        self.robot = pin_robot

    def warmup(self, thread_head):
        return

    def rnea(self, q, dq, ddq):
        return pin.rnea(self.robot.model, self.robot.data, q, dq, ddq)

    def run(self, thread_head):
        P = 3 * np.ones(3)
        D = 0.05 * np.ones(3)

        des_position = self.shared_vars.get("leader_pos")
        des_velocity = self.shared_vars.get("leader_vel")
        
        self.tau = (
            P * (des_position - self.joint_positions)
            + D * (des_velocity - self.joint_velocities)
        )

        self.tau += self.rnea(des_position,
                              self.zeros_pos, self.zeros_pos)
        self.head.set_control("ctrl_joint_torques", self.tau)
        return
