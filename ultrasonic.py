from threading import Thread
from threading import Event
from manual_control import reset_servo_angles
import time
from picarx import Picarx


def read_ultrasonic(stop_condition: Event,picar:Picarx):

    #global picar
    sensor = picar.ultrasonic
    while not stop_condition.is_set():
        try:
            distance = sensor.read()

            if distance < 25 and distance > 0:
                picar.stop()

                while distance < 25:
                    time.sleep(.25)
                    distance = sensor.read()
                    
                picar.forward(5)

        except Exception as e:
            print("Sensor error:", e)
            reset_servo_angles()
        time.sleep(0.25)