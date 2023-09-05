import cv2
import pytesseract
from pytesseract import Output

import re
import requests

LANG = "eng_tess"
CONFIG = (
    "--psm 6 --oem 2 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\\-"
)
CONF_THRESHOLD = 60

SERVER_URL = "http://localhost:9487"
PARAM_NAME = "A"

TEXT_PATTERN = "\\d{5}-[A-Z\\d]"


def send_request(text: str):
    m = re.search(f"({TEXT_PATTERN})", text)
    if not m:
        return
    result = m.group(0)
    if result:
        try:
            requests.get(SERVER_URL, {PARAM_NAME: result})
            print(["[send_request]"])
        except Exception as e:
            print("[send_request error]:")
            print(e)


def main():
    cv2.startWindowThread()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

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
