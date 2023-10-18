import cv2

import config
import telegram
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Cannot open camera')
    exit()

def draw_rect(frame, x: int, y: int, width: int, height: int) -> None:
    cv2.rectangle(
        frame,
        (x, y),
        (x + height, y + width),
        (0, 255, 0),
        5
    )

    cv2.putText(
        frame,
        'X: ' + str(x) + '; Y: ' + str(y) + '; WIDTH: ' + str(width) + '; HEIGHT: ' + str(height),
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        .5,
        (0, 255, 0),
        1
    )

def draw_date(frame) -> None:
    cv2.putText(
        frame,
        time.strftime('%Y-%m-%d %H:%M:%S'),
        (5, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )


while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print('Can`t receive frame (stream end?). Exiting ...')
        break

    if cv2.waitKey(1) == ord('q'):
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    found = classifier.detectMultiScale(
        image=gray,
        minNeighbors=6,
        minSize=config.MIN_SIZE,
        maxSize=config.MAX_SIZE
    )

    for (x, y, width, height) in found:
        draw_rect(frame, x, y, width, height)

        draw_date(frame)

    if len(found):
        print('DETECTED', time.strftime('%Y-%m-%d %H:%M:%S'))
        telegram.sendPhoto(cv2.imencode('.jpg', frame)[1])

    config.DEVELOP and cv2.imshow('cam', frame)
    time.sleep(config.TIMEOUT_SEC)

cap.release()
cv2.destroyAllWindows()
