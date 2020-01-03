# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array, traceback, time
from fcntl import ioctl
from DCMotors import DCMotors # import driver class for the DC Motors (DCmotors.py) 
from PCA9685 import PCA9685 # import servo driver class
from Buzzer import Buzzer # impor driver class for Buzzer

class PS4C_LJS():

    def __init__(self,debug=True):
        self.DEBUG=debug

    def setup(self):
        
        try:

            # Iterate over the joystick devices.
            print('Available devices:')

            for fn in os.listdir('/dev/input'):
                if fn.startswith('js'):
                    print(('  /dev/input/%s' % (fn)))

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
                0x06 : 'trottle',
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
            if self.DEBUG==True:
                print(('Opening %s...' % fn))
            jsdev = open(fn, 'rb')
            
            # Get the device name.
            #buf = bytearray(63)
            buf = array.array('B', [0] * 64)
            ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
            js_name = buf.tostring().rstrip(b'\x00').decode('utf-8')
            if self.DEBUG==True:
                print(('Device name: %s' % js_name))
                    
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


            # Print out the values
            if self.DEBUG==True:
                print(('%d axes found: %s' % (num_axes, ', '.join(axis_map))))
                print(('%d buttons found: %s' % (num_buttons, ', '.join(button_map))))


            ## CONFIGURE ANALOGUE JOYSTICK "DEAD-ZONES"
            # use these values to increase/decrease the deadzones on the analogues
            pdz=0.100 # Positve Deadzone
            ndz=-0.100 # Negative Deadzone

            ## Init the DCmotors class
            if self.DEBUG==True:
                print("Creating New DC Motor Class...")
            dcm = DCMotors()

            ## Init the PCA9685 class (Servo Motors)
            if self.DEBUG==True:
                print("Creating New Instance Of PCA9685 Class...")
            pwm=PCA9685(0x40, debug=True) # leave these aguments as is, do not change.
            pwm.setPWMFreq(50) #set the frequency | must be 50, do not chnage this!
            #set the initial servo pulses, which "center" the servos before we begin
            pwm.setServoPulse(0,1500) #horizontal | note: the channel (0) is for horizontal
            pwm.setServoPulse(1,1500) #vertical | note: the channel (1) is for vertical
            vslv=1500 # Vertical Servo Last Value | store the last known value for the vertical servo's 'Servo Pulse' | set to 1500 (center) before the main loop starts
            hslv=1500 # Horizontal Servo Last Value | store the last known value for the horizontal servo's 'Servo Pulse' | set to 1500 (center) before the main loop starts
            sspa=700 # Servo Stopping Point A | set the stopping point for the servo's here
            sspb=2300 # Servo Stopping Point B | set the stopping point for the servo's here
            sss=10 # Servo Step Size | set the size of the servo steps here (larger steps will make it move faster)

            ## Init the Buzzer class
            bzr=Buzzer()
            
            # Main event loop
            while True:
                evbuf = jsdev.read(8)
                if evbuf:
                    time, value, type, number = struct.unpack('IhBB', evbuf)
                            
                    if type & 0x80:
                        if self.DEBUG==True:
                            print("(initial)")
                                
                    if type & 0x01:
                        button = button_map[number]
                        if button:
                            button_states[button] = value
                            if value:
                                if self.DEBUG==True:
                                    print(("%s pressed" % (button)))
                            else:
                                if self.DEBUG==True:
                                    print(("%s released" % (button)))

                            ###############################################################
                            # BUTTONS [TRIANGLE, SQUARE, CROSS, CIRCLE] | MISC. FUNCTIONS #
                            ###############################################################

                            ## recenter the servos (SQUARE)
                            if value:
                                if button == "y":
                                    
                                    print(value)

                                    print("SQUARE Pushed... Centering Servos Now ^_^)")
                                    # set the servo pulse to the center positions/values for the vertical and horizontal servos
                                    pwm.setServoPulse(0,1500)
                                    pwm.setServoPulse(1,1500)
                                    # make sure the vertical & horizontal servo's last known value is reset to the 'center' position to prevent "jumping behaviour" when panning again
                                    vslv=1500
                                    hslv=1500

                            ## buzzer
                            if value:
                                if button == "b":

                                    print(value)
                                    
                                    print("CIRCLE Pushed... Buzzing Now ^_^")
                                    bzr.start()
                            else:
                                bzr.stop()
                                    
                                        
                    if type & 0x02:
                        axis = axis_map[number]
                        if axis:
                            fvalue = value / 32767.0
                            axis_states[axis] = fvalue
                            if self.DEBUG==True:
                                print(("%s: %.3f" % (axis, fvalue)))

                            ####################################
                            # LEFT ANALOGUE | DC MOTOR CONTROL #
                            ####################################
                            
                            ## forward
                            if axis == "y" and fvalue < ndz:
                                dcm.forward()
                                if self.DEBUG==True:
                                    print("Moving Forward...")
                            elif axis == "y" and fvalue == 0:
                                dcm.stop()
                                if self.DEBUG==True:
                                    print("Stopping...")

                            ## backward
                            elif axis == "y" and fvalue > pdz:
                                dcm.backward()
                                if self.DEBUG==True:
                                    print("Moving Backward...")
                            elif axis == "y" and fvalue == 0:
                                dcm.stop()
                                if self.DEBUG==True:
                                    print("Stopping...")

                            ## left
                            elif axis == "x" and fvalue < ndz:
                                dcm.left()
                                if self.DEBUG==True:
                                    print("Turning Left")
                            elif axis == "x" and fvalue == 0:
                                dcm.stop()
                                if self.DEBUG==True:
                                    print("Stopping...")
                                
                            ## right
                            elif axis == "x" and fvalue > pdz:
                                dcm.right()
                                if self.DEBUG==True:
                                    print("Turning Right")
                            elif axis == "x" and fvalue == 0:
                                dcm.stop()
                                if self.DEBUG==True:
                                    print("Stopping...")

                            ########################################
                            # RIGHT ANALOGUE | SERVO MOTOR CONTROL #
                            ########################################

                            ## up
                            if axis == "ry" and fvalue > pdz:
                                if vslv > sspa and vslv <= sspb: #make sure we are between a reasonable range
                                    vslv=vslv-sss # decrement our servo pulse
                                    if self.DEBUG==True:
                                        print("Panning Servo Up...")
                                        print("vslv:",vslv)
                                    pwm.setServoPulse(1,vslv)
                                    
                            ## down
                            elif axis == "ry" and fvalue < ndz:
                                if vslv >= sspa and vslv < sspb: #make sure we are between a reasonable range
                                    vslv=vslv+sss # increment our servo pulse
                                    if self.DEBUG==True:
                                        print("Panning Servo Down...")
                                        print("vslv:",vslv)
                                    pwm.setServoPulse(1,vslv)

                            ## left
                            elif axis == "rx" and fvalue < ndz:
                                if hslv >= sspa and hslv < sspb: #make sure we are between a reasonable range
                                    hslv=hslv+sss # decrement our servo pulse
                                    if self.DEBUG==True:
                                        print("Panning Servo Left...")
                                        print("hslv:",hslv)
                                    pwm.setServoPulse(0,hslv)
                                
                            ## right
                            elif axis == "rx" and fvalue > pdz:
                                if hslv > sspa and hslv <= sspb: #make sure we are between a reasonable range
                                    hslv=hslv-sss # increment our servo pulse
                                    if self.DEBUG==True:
                                        print("Panning Servo Right...")
                                        print("hslv:",hslv)
                                    pwm.setServoPulse(0,hslv)
                            
        except KeyboardInterrupt:
            print("Program stopped by user...")

        except Exception:
            traceback.print_exc()
            
        finally:
            if self.DEBUG==True:
                print("Setup process complete")

if __name__ == '__main__':

    print("Starting Test Now...")

    try:
        
        print("Creating Controller Instance")
        PS4C=PS4C_LJS()

        
        print("Running setup method for controller")
        print("Starting 'main loop' now...")
        PS4C.setup()
        
    except Exception:
        print("Something crappy happened!")
        traceback.print_exc()

    finally:
        print("Ending PS4 Controller Program Now...")
