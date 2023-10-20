import cv2
import time

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
