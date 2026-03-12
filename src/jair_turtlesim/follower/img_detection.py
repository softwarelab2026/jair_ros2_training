import cv2
import numpy as np


def extract_ball_pos(frame: np.ndarray) -> tuple[int, int]:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    _, mask = cv2.threshold(blurred, 75, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        area_pos = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(area_pos)

        if radius > 5:
            return (int(x), int(y))
    return (0, 0)
