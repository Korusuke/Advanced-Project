import time
import socket                                         
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig0, NYUFingerDoubleConfig1
from dynamic_graph_head import ThreadHead

from utils import GravityCompensationController

def start_hw_thread():
    head = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig0.dgm_yaml_path)

    pin_robot = NYUFingerDoubleConfig0.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    grav_ctrl = GravityCompensationController(head, pin_robot)

    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl],  # Safety controllers.
        {'head': head},  # Heads to read / write from.
        [],
    )
    thread_head.start()
    thread_head.switch_controllers([grav_ctrl])
    
    return head


if __name__ == "__main__":

    # start socket thread
    # start main program
    robot_head = start_hw_thread()

    
    # while True:
    #     joint_positions = robot_head.get_sensor("joint_positions")
    #     joint_velocities = robot_head.get_sensor("joint_velocities")
    #     print(joint_positions, joint_velocities)
    #     time.sleep(0.001)