from UDPComms import Publisher, Subscriber, timeout
from PS4Joystick import Joystick
import os, struct, array
from fcntl import ioctl
import time
import pickle
import socket

# Initialising UDP port and ip

UDP_IP = "192.168.0.183"
UDP_PORT = 9999
UDP_PORT2 = 6666

# Initialising the socket object

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 


dummy_msg = pickle.dumps({
    "btn1": 1,
    "btn2": -1,
    "btn3": 0.5,
    "btn4": -0.48
})

### code from js

# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'throttle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# Get the device name.
#buf = bytearray(63)
buf = array.array('B', [0] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

print('%d axes found: %s' % (num_axes, ', '.join(axis_map)))
print('%d buttons found: %s' % (num_buttons, ', '.join(button_map)))


###




## you need to git clone the PS4Joystick repo and run `sudo bash install.sh`

## Configurable ##
MESSAGE_RATE = 20
PUPPER_COLOR = {"red":0, "blue":0, "green":255}

# joystick_pub = Publisher(8830)
#joystick_subcriber = Subscriber(8840, timeout=0.01)
#joystick = Joystick()

#joystick.led_color(**PUPPER_COLOR)


left_y = 0
left_x = 0
right_x = 0
right_y = 0
L2 = 0
R2 = 0
R1 = 0
L1 = 0
dpady = 0
dpadx = 0
x = 0
square = 0
circle = 0
triangle = 0
MESSAGE_RATE = 20


def main_loop():
    while True:
        print("running the main event loop")
        values = joystick.get_input()

        left_y = -values["left_analog_y"]
        right_y = -values["right_analog_y"]
        right_x = values["right_analog_x"]
        left_x = values["left_analog_x"]

        L2 = values["l2_analog"]
        R2 = values["r2_analog"]

        R1 = values["button_r1"]
        L1 = values["button_l1"]

        square = values["button_square"]
        x = values["button_cross"]
        circle = values["button_circle"]
        triangle = values["button_triangle"]

        dpadx = values["dpad_right"] - values["dpad_left"]
        dpady = values["dpad_up"] - values["dpad_down"]

        msg = {
            "ly": left_y,
            "lx": left_x,
            "rx": right_x,
            "ry": right_y,
            "L2": L2,
            "R2": R2,
            "R1": R1,
            "L1": L1,
            "dpady": dpady,
            "dpadx": dpadx,
            "x": x,
            "square": square,
            "circle": circle,
            "triangle": triangle,
            "message_rate": MESSAGE_RATE,
        }
        joystick_pub.send(msg)

        try:
            msg = joystick_subcriber.get()
            joystick.led_color(**msg["ps4_color"])
        except timeout:
            pass

        time.sleep(1 / MESSAGE_RATE)




controller_dataframe = {
    "ly": left_y,
    "lx": left_x,
    "rx": right_x,
    "ry": right_y,
    "L2": L2,
    "R2": R2,
    "R1": R1,
    "L1": L1,
    "dpady": dpady,
    "dpadx": dpadx,
    "x": x,
    "square": square,
    "circle": circle,
    "triangle": triangle,
    "message_rate": MESSAGE_RATE
}


def main_loop2():
    while True:
        evbuf = jsdev.read(8)
        if evbuf:
            time, value, type, number = struct.unpack('IhBB', evbuf)

            if type & 0x80:
                print("(initial)", end="")
                left_y = 0
                left_x = 0
                right_x = 0
                right_y = 0
                L2 = 0
                R2 = 0
                R1 = 0
                L1 = 0
                dpady = 0
                dpadx = 0
                x = 0
                square = 0
                circle = 0
                triangle = 0
                MESSAGE_RATE = 20

            if type & 0x01:
                button = button_map[number]
                if button:
                    button_states[button] = value
                    if value:
                        print("%s pressed" % (button))
                        ######################################

                        if button == "a":
                            print("[DEBUG]  x")
                            x = 1
                        if button == "b":
                            print("[DEBUG]  circle")
                            circle = 1
                        if button == "x":
                            print("[DEBUG]  square")
                            square = 1
                        if button == "y":
                            print("[DEBUG]  triangle")
                            triangle = 1
                        if button == "tr":
                            print("[DEBUG]  tr")
                            R1 = 1
                        if button == "tl":
                            print("[DEBUG]  tl")
                            L1 = 1

                        if button == "select":
                            print("[DEBUG]  select")
                        if button == "start":
                            print("[DEBUG]  start")
                        if button == "thumbl":
                            print("[DEBUG]  thumbl")
                        if button == "thumbr":
                            print("[DEBUG]  thumbr")
                        if button == "mode":
                            print("[DEBUG]  mode")
                        

                        ######################################
                        # joystick_pub.send({"button":button})
                        # sock.sendto(dummy_msg, (UDP_IP, UDP_PORT))

                    else:
                        print("%s released" % (button))

                        if button == "a":
                            print("[DEBUG]  x")
                            x = 0
                        if button == "b":
                            print("[DEBUG]  circle")
                            circle = 0
                        if button == "x":
                            print("[DEBUG]  square")
                            square = 0
                        if button == "y":
                            print("[DEBUG]  triangle")
                            triangle = 0
                        if button == "tr":
                            print("[DEBUG]  tr")
                            R1 = 0
                        if button == "tl":
                            print("[DEBUG]  tl")
                            L1 = 0
                            
                        if button == "select":
                            print("[DEBUG]  select")
                        if button == "start":
                            print("[DEBUG]  start")
                        if button == "thumbl":
                            print("[DEBUG]  thumbl")
                        if button == "thumbr":
                            print("[DEBUG]  thumbr")
                        if button == "mode":
                            print("[DEBUG]  mode")
                        # joystick_pub.send({"button":button})
                        # sock.sendto(dummy_msg, (UDP_IP, UDP_PORT))

            if type & 0x02:
                axis = axis_map[number]
                if axis:
                    fvalue = value / 32767.0
                    # axis_states[axis] = fvalue
                    # print("%s: %.3f" % (axis, fvalue))
                    if axis == "y":
                        left_y = -fvalue
                        print("[DEBUG]  left_y: %.3f" % (left_y))
                    if axis == "x":
                        left_x = fvalue
                        print("[DEBUG]  left_x: %.3f" % (left_x))
                    if axis == "ry":
                        right_y = -fvalue
                        print("[DEBUG]  right_y: %.3f" % (right_y))
                    if axis == "rx":
                        right_x = fvalue
                        print("[DEBUG]  right_x: %.3f" % (right_x))

                    if axis == "z":
                        L2 = fvalue
                        print("[DEBUG]  LT: %.3f" % (L2))
                    if axis== "rz":
                        R2 = fvalue
                        print("[DEBUG]  RT: %.3f" % (R2))
                    if axis == "hat0x":
                        dpadx = fvalue
                        print("[DEBUG]  dpadx: %.3f" % (dpadx))
                    if axis == "hat0y":
                        dpady = fvalue
                        print("[DEBUG]  dpady: %.3f" % (dpady))
                    # sock.sendto(dummy_msg, (UDP_IP, UDP_PORT))

            controller_dataframe = {
                "ly": left_y,
                "lx": left_x,
                "rx": right_x,
                "ry": right_y,
                "L2": L2,
                "R2": R2,
                "R1": R1,
                "L1": L1,
                "dpady": dpady,
                "dpadx": dpadx,
                "x": x,
                "square": square,
                "circle": circle,
                "triangle": triangle,
                "message_rate": MESSAGE_RATE
            }
            # No floating point operation is performed deadzone checking
            if (controller_dataframe["ly"] < 0.01 or controller_dataframe["ly"] > -0.01):
                controller_dataframe["ly"] = 0
            if (controller_dataframe["lx"] < 0.01 or controller_dataframe["lx"] > -0.01):
                controller_dataframe["lx"] = 0

            if (controller_dataframe["ry"] < 0.01 or controller_dataframe["ry"] > -0.01):
                controller_dataframe["ry"] = 0
            if (controller_dataframe["rx"] < 0.01 or controller_dataframe["rx"] > -0.01):
                controller_dataframe["rx"] = 0 
            controller_dataframe = pickle.dumps(controller_dataframe)
            sock.sendto(controller_dataframe, (UDP_IP, UDP_PORT))
            sock.sendto(controller_dataframe, (UDP_IP, UDP_PORT2))

#main_loop()
main_loop2()
