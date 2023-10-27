import cv2
import config
import draw
import telegram
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Cannot open camera')
    exit()

last_telegram_update_id = None

while cap.isOpened():
    ret, frame = cap.read()
    is_photo_sent = False

    if not ret:
        print('Can`t receive frame (stream end?). Exiting ...')
        break

    if config.DEVELOP and cv2.waitKey(1) == ord('q'):
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

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

        telegram.send_photo(cv2.imencode('.jpg', frame)[1])
        is_photo_sent = True

    if config.DEVELOP:
        cv2.imshow('cam', frame)

    for update in telegram.get_updates(last_telegram_update_id):
        update_id = update.get('update_id')

        if update_id and update_id != last_telegram_update_id:
            last_telegram_update_id = update_id
            chat_id = update.get('message', {}).get('chat', {}).get('id')
            text = update.get('message', {}).get('text')

            if text and chat_id and chat_id in config.TELEGRAM_CHAT_IDS:
                if not is_photo_sent and text:
                    telegram.send_photo(cv2.imencode('.jpg', frame)[1])

    time.sleep(config.TIMEOUT_SEC)

cap.release()
cv2.destroyAllWindows()
