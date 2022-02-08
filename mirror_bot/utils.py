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

