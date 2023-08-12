import cv2
import pytesseract
from pytesseract import Output
from picamera2 import Picamera2

import re
import requests

LANG = "label"
CONFIG = (
    "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\\-"
)
CONF_THRESHOLD = 60

SERVER_URL = "http://localhost:9487"
PARAM_NAME = "A"

TEXT_PATTERN = "\\d{5}-[A-Z]"


def send_request(text: str):
    m = re.search(f"({TEXT_PATTERN})", text)
    if not m:
        return
    result = m.group(0)
    if result:
        # hacky way to ignore response
        try:
            requests.get(SERVER_URL, {PARAM_NAME: result}, timeout=0.0000000001)
        except Exception:
            pass


def main():
    picam2 = Picamera2()
    picam2.configure(
        picam2.create_preview_configuration(
            main={"format": "XRGB8888", "size": (320, 240)}
        )
    )
    picam2.start()

    cv2.startWindowThread()

    while True:
        frame = picam2.capture_array()

        d = pytesseract.image_to_data(
            frame, output_type=Output.DICT, lang=LANG, config=CONFIG
        )
        n_boxes = len(d["text"])
        for i in range(n_boxes):
            if int(d["conf"][i]) > CONF_THRESHOLD:
                (text, x, y, w, h) = (
                    d["text"][i],
                    d["left"][i],
                    d["top"][i],
                    d["width"][i],
                    d["height"][i],
                )
                if text and text.strip() != "":
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frame = cv2.putText(
                        frame,
                        text,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 0, 255),
                        3,
                    )

                    send_request(text)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
