import cv2
import config
import draw
import telegram
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Cannot open camera')
    exit()

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

    if len(found):
        print('DETECTED', time.strftime('%Y-%m-%d %H:%M:%S'))
        draw.draw_date(frame)

        for (x, y, width, height) in found:
            draw.draw_rect(frame, x, y, width, height)

        telegram.sendPhoto(cv2.imencode('.jpg', frame)[1])

    if config.DEVELOP:
        cv2.imshow('cam', frame)

    time.sleep(config.TIMEOUT_SEC)

cap.release()
cv2.destroyAllWindows()
