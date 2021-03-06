import cv2
import sys
import logging as log
import datetime as dt
from time import sleep

cascPath = r"haarcascade_frontalface_default.xml"
SMILE_CASCADE = cv2.CascadeClassifier(r"haarcascade_smile.xml")
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0
img_counter = 1
while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        region_of_interest_bw = gray[y:y + h, x:x + w]
        region_of_interest_color = frame[y:y + h, x:x + w]
        smiles = SMILE_CASCADE.detectMultiScale(region_of_interest_bw, 1.7, 22)
        for sx, sy, sw, sh in smiles:
            cv2.rectangle(region_of_interest_color, (sx, sy),
                          (sx + sw, sy + sh), (0, 0, 255), 2)

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

    # Display the resulting frame
    cv2.imshow('Video', frame)
    k = cv2.waitKey(1)
    if k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    if cv2.waitKey(1) & 0xFF == ord('s'):

        check, frame = video_capture.read()
        cv2.imshow("Capturing", frame)
        cv2.imwrite(filename='saved_img.jpg', img=frame)
        video_capture.release()
        img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
        img_new = cv2.imshow("Captured Image", img_new)
        cv2.waitKey(1650)
        print("Image Saved")
        print("Program End")
        cv2.destroyAllWindows()

        break
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        print("Turning off camera.")
        video_capture.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break


    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
