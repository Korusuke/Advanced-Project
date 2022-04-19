import time
import socket
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig0, NYUFingerDoubleConfig1
from dynamic_graph_head import ThreadHead
import numpy as np

from utils import (GravityCompensationControllerWithFeedback,
                   MirrorHeadGravityControllerForceFeedback)

import sys
import os
sys.path.append(os.path.abspath('../graphing'))
import grapher

shared_vars = {'leader_pos': np.array([0., 0., 0.]), 'leader_vel': np.array([0., 0., 0.]),
               'follower_pos': np.array([0., 0., 0.]), 'follower_vel': np.array([0., 0., 0.])}


def leader():
    global shared_vars
    head = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig0.dgm_yaml_path)

    pin_robot = NYUFingerDoubleConfig0.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    grav_ctrl = GravityCompensationControllerWithFeedback(
        head, pin_robot, shared_vars)

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
    copy_ctrl = MirrorHeadGravityControllerForceFeedback(
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
    # start grapher
    g = grapher.Grapher(sampleinterval=0.1, timewindow=10., datafeed=shared_vars)
    g.run()
