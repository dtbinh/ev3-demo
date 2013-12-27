import BaseHTTPServer
import urlparse
from threading import Timer;

import sys, re
sys.path.append('lib/ev3')
from ev3.rawdevice import motordevice




class RobotControlHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):


    def do_GET(self):
        """Respond to a GET request."""
        self.commands_queue = []
        self.currnet_group_size = 0;
        self.currnet_group_done_count = 0;

        parsed_path = urlparse.urlparse(self.path)
        todo = urlparse.parse_qs(parsed_path.query)['do'][0]
        print "<HTTP GET>: Recived command sequence ( " + todo + " )"
        commands_group_strings = todo.split('>')
        self.commands_queue = [commands_group_string.split("|") for commands_group_string in commands_group_strings]
        self.commands_queue.reverse()
        print "<HTTP GET>: Commands queue " + str(self.commands_queue)

        # self.run_all_commands(sequence)
        self.run_next_command_grup()

    def run_next_command_grup(self):
        if len(self.commands_queue) > 0:
            next_command = self.commands_queue.pop()
            print "<run_next_command_grup>: Running next command " + str(next_command)
            self.run_commands_in_parallel(next_command)
        else:
            print "<run_next_command_grup>: Sequence done!\n"

    def run_all_commands(self, commands):
        for i in range(len(commands)):
            command = commands[i].split(",")
            if self.is_valid_command(command):
                self.run_command(command)

    def run_command_sequence(self, sequence):
        for i in range(len(sequence)):
            parallel_commands = sequence[i].split("|")
            run_commands_in_parallel(parallel_commands)
            # if is_valid_command(command):
            #     run_command(command)

    def run_commands_in_parallel(self, commands):
        print "<run_commands_in_parallel>: Running command group " + str(commands)
        self.currnet_group_done_count = 0
        self.currnet_group_size = len(commands)
        for cmdStr in commands:
            cmd = cmdStr.split(",")
            if self.is_valid_command(cmd):
                self.run_command(cmd)

    def is_valid_command(self, command):
        if len(command) != 4:
            return False

        motor = command[0]
        if not motor in ["L", "R"]:
            print "<is_valid_command>: Command \"" + str(command) + "\"is not valid!   \"" + str(command[0]) + "\" is not a valid motor id"
            return False

        dir = command[1]
        if not dir in ["F", "B"]:
            print "<is_valid_command>: Command \"" + str(command) + "\"is not valid!   \"" + str(command[1]) + "\" is not a valid diraction"
            return False

        if not command[2].isdigit():
            print "<is_valid_command>: Command \"" + str(command) + "\"is not valid!   \"" + str(command[2]) + "\" is not a valid power"
            return False
        power = int(command[2])
        if  power < 0 or power > 100:
            print "<is_valid_command>: Command \"" + str(command) + "\"is not valid!   \"" + str(command[2]) + "\" is not a valid power"
            return False

        fr = re.compile('\d+(\.\d+)?')
        if fr.match(command[3]) == None:
            print "<is_valid_command>: Command \"" + str(command) + "\"is not valid!   \"" + str(command[3]) + "\" is not a valid duration"
            return False

        return True

    def run_command(self, command):
        print "<run_command>: Running command: " + str(command)
        global robot

        if command[0] == "R":
            motor = Robot.RIGHT_MOTOR
        elif command[0] == "L":
            motor = Robot.LEFT_MOTOR

        if command[1] == "F":
            dir = Robot.FORWARD
        elif command[1] == "B":
            dir = Robot.BACKWARD

        power = int(command[2])

        duration = float(command[3])

        robot.power_motor(motor, dir, power, duration, self.on_command_done);

    def on_command_done(self):
        self.currnet_group_done_count += 1
        print "<on_command_done>: " + str(self.currnet_group_done_count) + "/" + str(self.currnet_group_size)
        if self.currnet_group_done_count == self.currnet_group_size:
            self.run_next_command_grup()



class Robot(object):
    # Mototrs:  A = 0x01, B = 0x02, C = 0x04, D = 0x08
    RIGHT_MOTOR = 0x04
    LEFT_MOTOR = 0x02

    FORWARD = 1
    BACKWARD = 0

    def __init__(self):
        motordevice.open_device()

    def power_motor(self, motor, dir, power, duration, stop_call_back):
        print "<Robot.power_motor>: " + str((motor, dir, power, duration))
        motordevice.polarity(motor, dir)
        motordevice.power(motor, power)
        stop_timer = Timer(duration, self.stop_motor, [motor, stop_call_back])
        stop_timer.start()

    def stop_motor(self, motor, stop_call_back):
        print "<Robot.stop_motor>: " + str(motor)
        # TODO polarity is not working properly
        motordevice.power(motor, 0)
        motordevice.polarity(motor, self.FORWARD)
        stop_call_back()


robot = Robot()

from BaseHTTPServer import HTTPServer
server = HTTPServer(('0.0.0.0', 9000), RobotControlHTTPRequestHandler)
server.serve_forever()