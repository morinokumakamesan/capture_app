import base64
import numpy as np
import cv2

def save_img(img_base64):
    #binary <- string base64
    img_binary = base64.b64decode(img_base64)
    #jpg <- binary
    img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
    #raw image <- jpg
    img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
    #デコードされた画像の保存先パス
    #ローカル実行の場合
    # image_file="./app/static/images/capture.jpg"
    #Renderで実行の場合
    image_file="/opt/render/project/src/capture_app/app/static/images/capture.jpg"

    #画像を保存
    cv2.imwrite(image_file, img)
    return "SUCCESS"