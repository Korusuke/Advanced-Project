from dynamic_graph_head import HoldPDController
import time
import numpy as np
import pinocchio as pin

from robot_properties_nyu_finger.config import NYUFingerDoubleConfig0, NYUFingerDoubleConfig1
from robot_properties_nyu_finger.wrapper import NYUFingerRobot
from bullet_utils.env import BulletEnv
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import ThreadHead, SimHead

# mode
mode = 'Hardware'  # Hardware / default: Environment

if mode == 'Hardware':
    # Create the dgm communication to the control process.
    head0 = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig0.dgm_yaml_path)
    head1 = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig1.dgm_yaml_path)
else:
    # ! Create a Pybullet simulation environment before any robots !
    env = BulletEnv()
    # Create a robot instance. This adds the robot to the simulator as well.
    config0 = NYUFingerDoubleConfig0()
    config1 = NYUFingerDoubleConfig1()

    finger0 = NYUFingerRobot(config=config0)
    finger1 = NYUFingerRobot(config=config1)

    head0 = SimHead(finger0, with_sliders=False)  # left
    head1 = SimHead(finger1, with_sliders=False)  # right

    # Add the robot to the env to update the internal structure of the robot
    # at every simulation steps.
    env.add_robot(finger0)
    env.add_robot(finger1)

# pinocchio robot wrapper
pin_robot_0 = NYUFingerDoubleConfig0.pin_robot
pin_robot_1 = NYUFingerDoubleConfig1.pin_robot

####################
# Controller Logic #
####################


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


hold_ctrl0 = HoldPDController(head0, 3., 0.05, False)
hold_ctrl1 = HoldPDController(head1, 3., 0.05, False)

grav_ctrl0 = GravityCompensationController(head0, pin_robot_0)
grav_ctrl1 = GravityCompensationController(head1, pin_robot_1)

if mode == 'Hardware':
    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl0, hold_ctrl1],  # Safety controllers.
        {'head0': head0, 'head1': head1},  # Heads to read / write from.
        [],
    )
else:
    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl0, hold_ctrl1],  # Safety controllers.
        {'head0': head0, 'head1': head1},  # Heads to read / write from.
        [],
        env
    )

thread_head.start()
thread_head.switch_controllers([grav_ctrl0, grav_ctrl1])