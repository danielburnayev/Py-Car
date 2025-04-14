from threading import Lock
import time
from picarx import Picarx
from threading import Thread
from threading import Event

        
def read_grayscale(stop_condition:Event,picar:Picarx):
    #[0,0,0] handle out of line scenario

    #[1,0,0] turn wheels to the left sharply
    #[1,1,0] turn wheels to the left slightly

    #[1,1,1] do nothing

    #[0,0,1] turn wheels to the right sharply
    #[0,1,1] turn wheels to the right slightly
     
     #[0,1,0] and [1,0,1] shouldn't be techinically possible
    sensor = picar.grayscale

    while not stop_condition.is_set():
        line_status = sensor.read_status()
        print(line_status)
        #--------- turn right -----------
        if line_status == [0,1,1]:
            picar.set_dir_servo_angle(15)
            time.sleep(.2)
            picar.set_dir_servo_angle(0)

        elif line_status == [0,0,1]:
            picar.set_dir_servo_angle(40)
            time.sleep(.4)
            picar.set_dir_servo_angle(0)
        #--------------------------------

        #-------- turn left --------------
        elif line_status == [1,1,0]:
            picar.set_dir_servo_angle(-15)
            time.sleep(.2)
            picar.set_dir_servo_angle(0)
        
        elif line_status == [1,0,0]:
            picar.set_dir_servo_angle(-40)
            time.sleep(.4)
            picar.set_dir_servo_angle(0)
        #---------------------------------

        #---- reposition on the line --------
        elif line_status == [0,0,0]: #no longer on the line at all
            picar.stop()
            picar.backward(5)
            time.sleep(.4)
            picar.set_dir_servo_angle(0)
            picar.forward(5)
        #-------------------------------------
        
        #no correction needed
        else:
            pass

        time.sleep(.1)