import cv2
import pytesseract
import os
from urllib.request import urlopen
import numpy as np
from PIL import Image


class ImageToText:
    def __init__(self, preprocess="thresh"):
        self.preprocess = preprocess

    def imageconverter(self, image_link):
        req = urlopen(image_link)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        # загрузить образ и преобразовать его в оттенки серого
        image = cv2.imdecode(arr, -1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # проверьте, следует ли применять пороговое значение для предварительной обработки изображения

        if self.preprocess == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # если нужно медианное размытие, чтобы удалить шум
        elif self.preprocess == "blur":
            gray = cv2.medianBlur(gray, 3)

        # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        custom_config = r'--oem 3 --psm 6 -l rus'
        text = pytesseract.image_to_string(Image.open(filename), config=custom_config)
        os.remove(filename)

        return text


if __name__ == "__main__":
    images = ImageToText(image_link='https://sun9-74.userapi.com/impg/1of1GmThbqydVwDOAD-3UzdPDxDbgRGYameBKA/YWLT6CbnvAs.jpg?size=700x581&quality=96&sign=fe29daf322516e756d12a7e050260dc5&type=album')
    # print(images.imageconverter())
