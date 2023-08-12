# Label Recognition

This is a label recognition code run on Raspberry Pi 3B+.

## Dependency

- python 3.9.2
- cv2
- pytesseract
- picamera2
- re
- requests

## Description

This code is based on self-trained data which located in `/traineddata`.

1. Find text in specific format. (refer to `TEXT_PATTERN` in `app.py`)
2. Send a request to specific url. (refer to `SERVER_URL`, `PARAM_NAME` in `app.py`)

You can also try to change `CONF_THRESHOLD` if you encounter some problem in recognition.

## Execution

```shell
python app.py
```

Press `Q` to exit.
