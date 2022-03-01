import time
import socket
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig0, NYUFingerDoubleConfig1
from dynamic_graph_head import ThreadHead

from utils import (GravityCompensationController,
                   MirrorHeadController,
                   MirrorVelocityPositionHWController,
                   MirrorHeadGravityController)


shared_vars = {'leader_pos': None, 'leader_vel': None}


def leader():
    global shared_vars
    head = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig0.dgm_yaml_path)

    pin_robot = NYUFingerDoubleConfig0.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    grav_ctrl = GravityCompensationController(head, pin_robot, shared_vars)

    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl],  # Safety controllers.
        {'head': head},  # Heads to read / write from.
        [],
    )
    thread_head.start()
    thread_head.switch_controllers([grav_ctrl])

    return head


def follower():
    global shared_vars
    head = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig1.dgm_yaml_path)

    pin_robot = NYUFingerDoubleConfig1.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    copy_ctrl = MirrorHeadGravityController(
        head, pin_robot, shared_vars)

    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl],  # Safety controllers.
        {'head': head},  # Heads to read / write from.
        [],
    )
    thread_head.start()
    thread_head.switch_controllers([copy_ctrl])

    return head


if __name__ == "__main__":

    # start leader program
    leader_head = leader()
    # start follower program
    follower_head = follower()
