# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array, traceback, time
from fcntl import ioctl
# from DCMotors import DCMotors # import driver class for the DC Motors (DCmotors.py)
from DCMotors_VS import DCMotors # import driver class for the DC Motors (DCmotors.py)
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
            # set speeds up here | use to set speed for DC Motors in the program
            dcm_speed_0=0
            dcm_speed_1=10
            dcm_speed_2=20
            dcm_speed_3=30
            dcm_speed_4=40
            dcm_speed_5=50
            # set initial speeds here
            dcm_initial_speed_x = dcm_speed_1 # Turning (Left/Right)
            dcm_initial_speed_y = dcm_speed_2 # Movement (Forward/Backward)
            # use initial speed values to set the initial Pulse Width Modulation values
            dcm.setPWMAX(dcm_initial_speed_x) # Turning (Left Wheel)
            dcm.setPWMBX(dcm_initial_speed_x) # Turning (Right Wheel)
            dcm.setPWMAY(dcm_initial_speed_y) # Moving Forward/Backward (Left Wheel)
            dcm.setPWMBY(dcm_initial_speed_y) # Moving Forward/Backward (Right Wheel)
            # store "last known" speeds here (starts with the 'initial speed' values)
            dcm_last_known_speed_x=dcm_initial_speed_x # Turning (Left/Right)
            dcm_last_known_speed_y=dcm_initial_speed_y # Movement (Forward/Backward)
            # store the "current" speeds here
            dcm_current_speed_x=dcm_initial_speed_x # Turning (Left/Right)
            dcm_current_speed_y=dcm_initial_speed_y # Movement (Forward/Backward)

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
                            if value:

                                ################################
                                # CIRCLE | RECENTER THE SERVOS #
                                ################################
                                if button == "b":
                                    
                                    print("CIRCLE Pushed... Centering Servos Now ^_^)")
                                    # set the servo pulse to the center positions/values for the vertical and horizontal servos
                                    pwm.setServoPulse(0,1500)
                                    pwm.setServoPulse(1,1500)
                                    # make sure the vertical & horizontal servo's last known value is reset to the 'center' position to prevent "jumping behaviour" when panning again
                                    vslv=1500
                                    hslv=1500

                                ##############################################
                                # SQUARE | RESET SPEEDS | TURNING & MOVEMENT #
                                ##############################################
                                elif button == "y":

                                    print("SQUARE Pushed... Resetting Speeds Now ^_^")
                                    ## reset speed code here...
                                    dcm.setPWMAX(dcm_initial_speed_x) # set Pulse Width Modulation For Motor A To Initial Value (Turning Speed)
                                    dcm.setPWMBX(dcm_initial_speed_x) # set Pulse Width Modulation For Motor B To Initial Value (Turning Speed)
                                    dcm.setPWMAY(dcm_initial_speed_y) # set Pulse Width Modulation For Motor A To Initial Value (Movement Speed)
                                    dcm.setPWMBX(dcm_initial_speed_y) # set Pulse Width Modulation For Motor B To Initial Value (Movement Speed)
                                    dcm_last_known_speed_x=dcm_initial_speed_x # update last known movement speed to the initial value (Turning Speed)
                                    dcm_last_known_speed_y=dcm_initial_speed_y # update last known movement speed to the initial value (Movement Speed)

                                ##########
                                # BUZZER #
                                ##########
                                elif button == "x":

                                    print("CIRCLE Pushed... Buzzing Now ^_^")
                                    bzr.ezbuzz()    

                                ###########################################################
                                # speed control (DC Motors) | MOVEMENT (FORWARD/BACKWARD) #
                                ###########################################################

                                ## SLOW DOWN (top left trigger)
                                elif button == "tl":

                                    print ("Top Left Trigger Pushed... Decreasing Speed now...")

                                    # if speed is zero, do nothing... cant slow down any more than that can we..
                                    if dcm_last_known_speed_y == dcm_speed_0:
                                        print("Speed is already 0, we cant go any lower bro...")

                                    # else if speed is 1, slow down to 0
                                    elif dcm_last_known_speed_y == dcm_speed_1:
                                        print("Slowing Down Turning Speed to: ",dcm_speed_0)
                                        dcm.setPWMAY(dcm_speed_0)
                                        dcm.setPWMBY(dcm_speed_0)
                                        dcm_last_known_speed_y=dcm_speed_0 # update last known speed value to the updated one

                                    # else if speed is 2, slow down to 1
                                    elif dcm_last_known_speed_y == dcm_speed_2:
                                        print("Slowing Down Turning Speed to: ",dcm_speed_1)
                                        dcm.setPWMAY(dcm_speed_1)
                                        dcm.setPWMBY(dcm_speed_1)
                                        dcm_last_known_speed_y=dcm_speed_1 # update last known speed value to the updated one
                                        
                                    # else if speed is 3, slow down to 2
                                    elif dcm_last_known_speed_y == dcm_speed_3:
                                        print("Slowing Down Turning Speed to: ",dcm_speed_2)
                                        dcm.setPWMAY(dcm_speed_2)
                                        dcm.setPWMBY(dcm_speed_2)
                                        dcm_last_known_speed_y=dcm_speed_2 # update last known speed value to the updated one

                                    # else if speed is 4, slow down to 3
                                    elif dcm_last_known_speed_y == dcm_speed_4:
                                        print("Slowing Down Turning Speed to: ",dcm_speed_3)
                                        dcm.setPWMAY(dcm_speed_3)
                                        dcm.setPWMBY(dcm_speed_3)
                                        dcm_last_known_speed_y=dcm_speed_3 # update last known speed value to the updated one

                                    # else if speed is 5, slow down to 4
                                    elif dcm_last_known_speed_y == dcm_speed_5:
                                        print("Slowing Down Turning Speed to: ",dcm_speed_4)
                                        dcm.setPWMAY(dcm_speed_4)
                                        dcm.setPWMBY(dcm_speed_4)
                                        dcm_last_known_speed_y=dcm_speed_4 # update last known speed value to the updated one
                                    
                                ## SPEED UP (top left trigger)
                                elif button == "tr":

                                    print ("Top Right Trigger Pushed... Increasing Speed now...")

                                    # if speed is 0, speed up to 1..
                                    if dcm_last_known_speed_y == dcm_speed_0:
                                        print("Speeding Up Turning Speed to: ",dcm_speed_1)
                                        dcm.setPWMAY(dcm_speed_1)
                                        dcm.setPWMBY(dcm_speed_1)
                                        dcm_last_known_speed_y=dcm_speed_1 # update last known speed value to the updated one

                                    # else if speed is 1, speed up to 2
                                    elif dcm_last_known_speed_y == dcm_speed_1:
                                        print("Speeding Up Turning Speed to: ",dcm_speed_2)
                                        dcm.setPWMAY(dcm_speed_2)
                                        dcm.setPWMBY(dcm_speed_2)
                                        dcm_last_known_speed_y=dcm_speed_2 # update last known speed value to the updated one

                                    # else if speed is 2, speed up to 3
                                    elif dcm_last_known_speed_y == dcm_speed_2:
                                        print("Speeding Up Turning Speed to: ",dcm_speed_3)
                                        dcm.setPWMAY(dcm_speed_3)
                                        dcm.setPWMBY(dcm_speed_3)
                                        dcm_last_known_speed_y=dcm_speed_3 # update last known speed value to the updated one

                                    # else if speed is 3, speed up to 4
                                    elif dcm_last_known_speed_y == dcm_speed_3:
                                        print("Speeding Up Turning Speed to: ",dcm_speed_4)
                                        dcm.setPWMAY(dcm_speed_4)
                                        dcm.setPWMBY(dcm_speed_4)
                                        dcm_last_known_speed_y=dcm_speed_4 # update last known speed value to the updated one

                                    # else if speed is 4, speed up to 5
                                    elif dcm_last_known_speed_y == dcm_speed_4:
                                        print("Speeding Up Turning Speed to: ",dcm_speed_5)
                                        dcm.setPWMAY(dcm_speed_5)
                                        dcm.setPWMBY(dcm_speed_5)
                                        dcm_last_known_speed_y=dcm_speed_5 # update last known speed value to the updated one

                                    # else if speed is 5, this is our max, so we wont go any higher...
                                    elif dcm_last_known_speed_y == dcm_speed_5:
                                        print("Speed is already 5, we cant go any higher bro... Maybe consider making a 'Temp Power Boost' function using a different button... L3 maybe? ;)")
                                        
                            else:
                                print(("%s released" % (button))) # this gets fired EVERYTIME a button is "released"
                                        
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

                            ############################################################
                            # HAT DIRECTIONAL BUTTONS | DC MOTOR TURNING SPEED CONTROL #
                            ############################################################

                            ### DOWN BUTTON
                            ## SLOW DOWN
                            if axis == "hat0y" and fvalue == 1:

                                print("hat0y (UP) Pushed...")
                                
                                # if speed is zero, do nothing... cant slow down any more than that can we..
                                if dcm_last_known_speed_x == dcm_speed_0:
                                    print("Speed is already 0, we cant go any lower bro...")

                                # else if speed is 1, slow down to 0
                                elif dcm_last_known_speed_x == dcm_speed_1:
                                    print("Slowing Down Turning Speed to: ",dcm_speed_0)
                                    dcm.setPWMAX(dcm_speed_0)
                                    dcm.setPWMBX(dcm_speed_0)
                                    dcm_last_known_speed_x=dcm_speed_0 # update last known speed value to the updated one

                                # else if speed is 2, slow down to 1
                                elif dcm_last_known_speed_x == dcm_speed_2:
                                    print("Slowing Down Turning Speed to: ",dcm_speed_1)
                                    dcm.setPWMAX(dcm_speed_1)
                                    dcm.setPWMBX(dcm_speed_1)
                                    dcm_last_known_speed_x=dcm_speed_1 # update last known speed value to the updated one

                                # else if speed is 3, slow down to 2
                                elif dcm_last_known_speed_x == dcm_speed_3:
                                    print("Slowing Down Turning Speed to: ",dcm_speed_2)
                                    dcm.setPWMAX(dcm_speed_2)
                                    dcm.setPWMBX(dcm_speed_2)
                                    dcm_last_known_speed_x=dcm_speed_2 # update last known speed value to the updated one

                                # else if speed is 4, slow down to 3
                                elif dcm_last_known_speed_x == dcm_speed_4:
                                    print("Slowing Down Turning Speed to: ",dcm_speed_3)
                                    dcm.setPWMAX(dcm_speed_3)
                                    dcm.setPWMBX(dcm_speed_3)
                                    dcm_last_known_speed_x=dcm_speed_3 # update last known speed value to the updated one

                                # else if speed is 5, slow down to 4
                                elif dcm_last_known_speed_x == dcm_speed_5:
                                    print("Slowing Down Turning Speed to: ",dcm_speed_4)
                                    dcm.setPWMAX(dcm_speed_4)
                                    dcm.setPWMBX(dcm_speed_4)
                                    dcm_last_known_speed_x=dcm_speed_4 # update last known speed value to the updated one

                            
                            ### UP BUTTON
                            ## SPEED UP
                            elif axis == "hat0y" and fvalue == -1:

                                print ("hat0y (DOWN) Pushed... Increasing Speed now...")

                                # if speed is 0, speed up to 1..
                                if dcm_last_known_speed_x == dcm_speed_0:
                                    print("Speeding Up Turning Speed to: ",dcm_speed_1)
                                    dcm.setPWMAX(dcm_speed_1)
                                    dcm.setPWMBX(dcm_speed_1)
                                    dcm_last_known_speed_x=dcm_speed_1 # update last known speed value to the updated one

                                # else if speed is 1, speed up to 2
                                elif dcm_last_known_speed_x == dcm_speed_1:
                                    print("Speeding Up Turning Speed to: ",dcm_speed_2)
                                    dcm.setPWMAX(dcm_speed_2)
                                    dcm.setPWMBX(dcm_speed_2)
                                    dcm_last_known_speed_x=dcm_speed_2 # update last known speed value to the updated one

                                # else if speed is 2, speed up to 3
                                elif dcm_last_known_speed_x == dcm_speed_2:
                                    print("Speeding Up Turning Speed to: ",dcm_speed_3)
                                    dcm.setPWMAX(dcm_speed_3)
                                    dcm.setPWMBX(dcm_speed_3)
                                    dcm_last_known_speed_x=dcm_speed_3 # update last known speed value to the updated one

                                # else if speed is 3, speed up to 4
                                elif dcm_last_known_speed_x == dcm_speed_3:
                                    print("Speeding Up Turning Speed to: ",dcm_speed_4)
                                    dcm.setPWMAX(dcm_speed_4)
                                    dcm.setPWMBX(dcm_speed_4)
                                    dcm_last_known_speed_x=dcm_speed_4 # update last known speed value to the updated one

                                # else if speed is 4, speed up to 5
                                elif dcm_last_known_speed_x == dcm_speed_4:
                                    print("Speeding Up Turning Speed to: ",dcm_speed_5)
                                    dcm.setPWMAX(dcm_speed_5)
                                    dcm.setPWMBX(dcm_speed_5)
                                    dcm_last_known_speed_x=dcm_speed_5 # update last known speed value to the updated one

                                # else if speed is 5, this is our max, so we wont go any higher...
                                elif dcm_last_known_speed_x == dcm_speed_5:
                                    print("Speed is already 5, we cant go any higher bro... Maybe consider making a 'Temp Power Boost' function using a different button... L3 maybe? ;)")
                                
                            
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
