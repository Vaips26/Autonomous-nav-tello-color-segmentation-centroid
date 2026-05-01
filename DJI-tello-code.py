import cv2
import numpy as np
from djitellopy import Tello
import time

tello = Tello()
tello.connect()
print(tello.get_battery())
tello.streamon()
frame_read = tello.get_frame_read()
width, height = 640, 480
tello.takeoff()
tello.move_up(20)
time.sleep(0.001)
tello.move_up(30)
time.sleep(0.001)
tello.move_up(25)
time.sleep(0.001)
tello.move_up(30)

time.sleep(0.001)

def movements(centroid_x, centroid_y):
    if centroid_x > width // 2 + 30:
        tello.send_rc_control(30, 0, 0, 0)
    elif centroid_x < width // 2 - 30:
        tello.send_rc_control(-30, 0, 0, 0)  
    else:
        tello.send_rc_control(0, 80, 0, 0)
        time.sleep(0.1)
        tello.send_rc_control(0, 30, 0, 0) 
        time.sleep(0.1)
        tello.send_rc_control(0, 40, 0, 0) 
        time.sleep(0.1)
        tello.send_rc_control(0, 0, 0, 0)
        time.sleep(0.1)

    if centroid_y < height // 2 - 30:
        tello.send_rc_control(0, 20, 0, 0)
    elif centroid_y > height // 2 + 30:
        tello.send_rc_control(0, -30, 0, 0) #estaba en menos 20
    else:
        tello.send_rc_control(0, 80, 0, 0)
        time.sleep(0.1)
        tello.send_rc_control(0, 30, 0, 0) #estaba en 20
        time.sleep(0.1)
        tello.send_rc_control(0, 40, 0, 0) 
        time.sleep(0.1)
        tello.send_rc_control(0, 0, 0, 0)
        time.sleep(0.1)

cv2.namedWindow("Deteccion de marcos naranjas", cv2.WINDOW_NORMAL)

no_orange_frames = 0  # Counter for consecutive frames with no orange detection
#rotate_angle = -40  # Angle to rotate when no orange is detected

while True:
    frame = frame_read.frame
    frame = cv2.resize(frame, (width, height))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([0, 70, 50])
    upper_orange = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        no_orange_frames += 1
        if no_orange_frames >= 3:  # Rotate when no orange detected for 4 consecutive frames
            tello.send_rc_control(0,0,0,0)
            time.sleep(0.001) 
            tello.send_rc_control(30, 0, 0, -40)
            tello.send_rc_control(0, 0, 0, -10)
            time.sleep(0.1)  # Adjust sleep time as needed for rotation add one 0 
            no_orange_frames = 0
    else:
        tello.send_rc_control(0, 0, 0, -40)
        tello.send_rc_control(0, 0, 0, -10)
        no_orange_frames = 0  # Reset the counter

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 3000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                centroid_x = x + int(w / 2)
                centroid_y = y + int(h / 2)
                cv2.circle(frame, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
                cv2.putText(frame, f'({centroid_x}, {centroid_y})', (centroid_x + 10, centroid_y + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                movements(centroid_x, centroid_y)

    cv2.imshow("Deteccion de marcos naranjas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.land()
tello.streamoff()
cv2.destroyAllWindows()