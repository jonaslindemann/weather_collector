import numpy as np
import cv2
import requests

class CameraCapture:
    def __init__(self):
        self.__camera_urls = []
        self.__auth = ('admin', 'Password01')
        self.__filename_template = 'cap-%03d.png'

    def add_url(self, url):
        self.__camera_urls.append(url)

    def capture(self):
        i = 1
        for url in self.__camera_urls:  
            print('Capturing : %s' % url)
            try:
                resp = requests.get('%s/streaming/channels/1/picture' % (url), auth=self.__auth)
                image = np.asarray(bytearray(resp.content), dtype='uint8')
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                cv2.imwrite(self.__filename_template % i, image)
            except:
                print('Couldn\'t aquire %s' % url)
                
            i+=1

if __name__ == "__main__":

    capture = CameraCapture()
    capture.add_url('http://192.168.0.191')
    capture.add_url('http://192.168.0.192')
    capture.add_url('http://192.168.0.193')
    capture.add_url('http://192.168.0.194')
    capture.capture()
