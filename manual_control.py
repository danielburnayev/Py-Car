import readchar
from picarx import Picarx
import time
from threading import Lock



def control_thread(lock: Lock,picar:Picarx,servo_angle):
    try:
        #global servo_angle, picar
        while True:
            char = readchar.readkey()
            if char == 'w':
                picar.forward(10)

            elif char == 's':
                picar.backward(10)
                time.sleep(0.05)

            elif char == 'a':
                with lock:
                    if servo_angle == -35: #prevent servo from turning too much
                        continue
                    servo_angle -=5 
                picar.set_dir_servo_angle(servo_angle)
                time.sleep(0.05)

            elif char == 'd':
                with lock:
                    if servo_angle == 35: #prevent servo from turning too much
                        continue
                servo_angle += 5
                picar.set_dir_servo_angle(servo_angle)
                time.sleep(0.05)

            elif char == 'f':
                picar.stop()

            elif char == 'q':
                reset_servo_angles(lock,picar,servo_angle)
                picar.stop()
                return
            
            elif char == 'z':
                reset_servo_angles(lock,picar,servo_angle)

            else:
                continue

            
    except KeyboardInterrupt:
        picar.stop()
        reset_servo_angles(lock,picar,servo_angle)
        return
    
def reset_servo_angles(lock:Lock,picar,servo_angle):
    #global servo_angle
    if servo_angle == 0:
        return
    with lock:
        if servo_angle < 0:
            for i in range(servo_angle,0,1):
                servo_angle += 1
                picar.set_dir_servo_angle(i)
                time.sleep(0.01)
        else:
            for i in range(servo_angle,0,-1):
                servo_angle -=1
                picar.set_dir_servo_angle(i)
                time.sleep(0.01)