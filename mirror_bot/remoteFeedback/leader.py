import time
import socket
import threading
import json
import numpy as np
import dynamic_graph_manager_cpp_bindings
from dynamic_graph_head import HoldPDController
from robot_properties_nyu_finger.config import NYUFingerDoubleConfig0
from dynamic_graph_head import ThreadHead

from utils import GravityCompensationControllerWithFeedback

import sys
import os
sys.path.append(os.path.abspath('../graphing'))
import grapher

shared_vars = {'leader_pos': np.array([0., 0., 0.]), 'leader_vel': np.array([0., 0., 0.]),
               'follower_pos': np.array([0., 0., 0.]), 'follower_vel': np.array([0., 0., 0.])}


def socket_process():
    global shared_vars
    sock = socket.socket()
    sock.bind(("127.0.0.1", 12346))
    sock.listen(3)
    print("Waiting for follower/s to connect")
    conn = sock.accept()
    print("Follower connected")
    print("Starting mirroring in 3 seconds")
    time.sleep(3)

    while True:
        serial_rec_data = conn[0].recv(4096)
        data = json.loads(serial_rec_data.decode('utf-8').strip())

        shared_vars['follower_pos'] = np.asarray(data['position'])
        shared_vars['follower_vel'] = np.asarray(data['velocity'])

        # Send my pos and vel
        my_pos = shared_vars['leader_pos'].tolist()
        my_vel = shared_vars['leader_vel'].tolist()
        data = {
            'position': my_pos,
            'velocity': my_vel,
            'time': time.time()
        }
        serial_data = json.dumps(data)
        conn[0].send(serial_data.encode())

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


def leader():
    global shared_vars
    head = dynamic_graph_manager_cpp_bindings.DGMHead(
        NYUFingerDoubleConfig0.dgm_yaml_path)

    pin_robot = NYUFingerDoubleConfig0.pin_robot

    hold_ctrl = HoldPDController(head, 3., 0.05, False)
    grav_ctrl = GravityCompensationControllerWithFeedback(head, pin_robot, shared_vars)

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
    # start socket
    thread = threading.Thread(target=socket_process)
    thread.daemon = True
    thread.start()

    # start leader program
    leader_head = leader()
    
    # start grapher
    g = grapher.Grapher(sampleinterval=0.1, timewindow=10., datafeed=shared_vars)
    g.run()
