import serial
import json
import queue
import threading
import time

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(512, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

class BaseController:
    def __init__(self, uart_dev_set, baud_set):
        self.ser = serial.Serial(uart_dev_set, baud_set, timeout=1)
        self.rl = ReadLine(self.ser)
        self.command_queue = queue.Queue()
        self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.command_thread.start()

        self.current_x = 0  

        self.x_min = -45
        self.x_max = 45

        self.y_fixed = 0

    def send_command(self, data):
        self.command_queue.put(data)

    def process_commands(self):
        while True:
            data = self.command_queue.get()
            self.ser.write((json.dumps(data) + '\n').encode("utf-8"))
            time.sleep(0.1)

    def gimbal_ctrl(self, input_x, input_y, input_speed=0, input_acceleration=0):
        input_x = max(self.x_min, min(self.x_max, input_x))
        input_y = self.y_fixed

        data = {
            "T": 133,
            "X": int(input_x),
            "Y": int(input_y),
            "SPD": input_speed,
            "ACC": input_acceleration
        }
        self.send_command(data)
        self.current_x = input_x

    def track_x(self, center_x, dead_zone=0.05, angle_threshold=1.0, speed=20, acceleration=10):
        error_x = center_x - 0.5
        if abs(error_x) < dead_zone:
            return

        target_x = error_x * 2 * self.x_max
        target_x = max(self.x_min, min(self.x_max, target_x))

        if abs(target_x - self.current_x) < angle_threshold:
            return

        self.gimbal_ctrl(target_x, self.y_fixed, input_speed=speed, input_acceleration=acceleration)
