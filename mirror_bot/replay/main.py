import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig0, NYUFingerDoubleConfig1
from dynamic_graph_head import ThreadHead

from datetime import datetime
from ast import While, arg
from utils import (getArgs,
                   RecorderController,
                   PlayBackController)


def recorder(robot, fileName):
    if robot == 1:
        head = dynamic_graph_manager_cpp_bindings.DGMHead(
            NYUFingerDoubleConfig0.dgm_yaml_path)

        pin_robot = NYUFingerDoubleConfig0.pin_robot

    if robot == 2:
        head = dynamic_graph_manager_cpp_bindings.DGMHead(
            NYUFingerDoubleConfig1.dgm_yaml_path)

        pin_robot = NYUFingerDoubleConfig1.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    grav_ctrl = RecorderController(head, pin_robot, fileName)

    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl],  # Safety controllers.
        {'head': head},  # Heads to read / write from.
        [],
    )
    thread_head.start()
    thread_head.switch_controllers([grav_ctrl])

    while True:
        try:
            x = input()
        except KeyboardInterrupt:
            break
    grav_ctrl.closeFile()
    return


def playback(robot, fileName):
    if robot == 1:
        head = dynamic_graph_manager_cpp_bindings.DGMHead(
            NYUFingerDoubleConfig0.dgm_yaml_path)

        pin_robot = NYUFingerDoubleConfig0.pin_robot

    if robot == 2:
        head = dynamic_graph_manager_cpp_bindings.DGMHead(
            NYUFingerDoubleConfig1.dgm_yaml_path)

        pin_robot = NYUFingerDoubleConfig1.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    play_ctrl = PlayBackController(head, pin_robot, fileName)

    thread_head = ThreadHead(
        0.001,  # dt.
        [hold_ctrl],  # Safety controllers.
        {'head': head},  # Heads to read / write from.
        [],
    )
    thread_head.start()
    thread_head.switch_controllers([play_ctrl])

    while True:
        try:
            x = input()
        except KeyboardInterrupt:
            break
    play_ctrl.closeFile()

    return


if __name__ == "__main__":
    # Record Mode
    # ./main.py record 1 filename

    # Play Mode
    # ./main.py play 2 test1
    args = getArgs()
    if args.type == 'record':
        print('Initializing Robot to Record actions')
    else:
        print('Initializing Robot to Playback actions')

    fileName = args.filename
    if args.filename is None:
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        fileName = f'record-{date_time}.actions'

    if args.type == 'record':
        recorder(args.robot, fileName)
    else:
        playback(args.robot, fileName)
