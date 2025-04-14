from ultrasonic import read_ultrasonic
from grayscale import read_grayscale
from manual_control import control_thread
from manual_control import reset_servo_angles

from threading import Thread
from threading import Lock
from threading import Event

from picarx import Picarx

lock =  Lock()
stop_condition = Event()
servo_angle = 0
picar = Picarx()

reset_servo_angles(lock,picar,servo_angle)
thread1 = Thread(target=control_thread,args=[lock,picar,servo_angle],daemon = True)
thread1.start()

thread2 = Thread(target=read_ultrasonic,args=[stop_condition,picar],daemon=True)
thread2.start()

#thread3 = Thread(target=read_grayscale,args=[stop_condition,picar],daemon=True)
#thread3.start()

thread1.join() #block main thread until thread1 terminates

stop_condition.set() #set event to signal other threads to terminate
reset_servo_angles(lock,picar,servo_angle)




