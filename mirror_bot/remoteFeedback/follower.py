import time
import socket
import threading
import json
import numpy as np
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig1
from dynamic_graph_head import ThreadHead

from utils import MirrorHeadGravityControllerForceFeedback


shared_vars = {'leader_pos': np.array([0., 0., 0.]), 'leader_vel': np.array([0., 0., 0.]),
               'follower_pos': np.array([0., 0., 0.]), 'follower_vel': np.array([0., 0., 0.])}


def socket_process():
    global shared_vars
    sock = socket.socket()
    print("Connecting to leader...")

    sock.connect(("127.0.0.1", 12346))
    print("Leader connected")
    print("Starting mirroring in 3 seconds")
    time.sleep(3)

    while True:
        my_pos = shared_vars['follower_pos'].tolist()
        my_vel = shared_vars['follower_vel'].tolist()
        data = {
            'position': my_pos,
            'velocity': my_vel,
            'time': time.time()
        }
        serial_data = json.dumps(data)

        sock.send(serial_data.encode())
        serial_rec_data = sock.recv(4096)
        data = json.loads(serial_rec_data.decode('utf-8').strip())

        shared_vars['leader_pos'] = np.asarray(data['position'])
        shared_vars['leader_vel'] = np.asarray(data['velocity'])

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


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
    # start socket
    thread = threading.Thread(target=socket_process)
    thread.daemon = True
    thread.start()
    # start follower program
    follower_head = follower()
