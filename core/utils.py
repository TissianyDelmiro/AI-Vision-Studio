import cv2
import numpy as np
import base64

def decode_image(data_url):
    try:
        if "," in data_url:
            _, encoded = data_url.split(",", 1)
        else:
            encoded = data_url
        data = base64.b64decode(encoded)
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except:
        return None

def encode_image(img, quality=70):
    # Converte qualidade de 0.0-1.0 (JS) para 0-100 (OpenCV) se necessário, 
    # mas aqui assumiremos que o app.py passará um valor de 0-100.
    _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
    encoded = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded}"
