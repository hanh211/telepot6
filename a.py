import sys
# pip install pyqt5
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
from ultralytics import YOLO
import telepot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.Button_start.clicked.connect(self.start_capture_video)

        self.thread = {}

    def start_capture_video(self):
        self.thread[1] = capture_video(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self, index):
        self.index = index
        # print("start threading", self.index)
        super(capture_video, self).__init__()

    def run(self):
        model = YOLO("yolov8n.pt")
        results = model("rtsp://admin:admin1234@ngduchanh.ddns.net:554/cam/realmonitor?channel=1&subtype=0",stream=True,show=True)
        for result,frame in results:
            self.signal.emit(frame)
            boxes=result[0].boxes
            for box in boxes.numpy():
                x=(box.xyxy[0][0]+box.xyxy[0][2])/2
                y=int(box.xyxy[0][1])+int(box.xyxy[0][3])/2
                b=(0,0)[0]<x<(800,500)[0] and (0,0)[1]<y<(800,500)[1]
                if b:
                    token = "6275415240:AAF3yDdT45-VIn8GdBrQUHH0XmtMXo0MC28"
                    receiver_id=5877612764
                    bot = telepot.Bot(token)
                    a=cv2.imwrite("a.jpg",frame)
                    bot.sendPhoto(receiver_id,photo=open("a.jpg", "rb"),caption="Có xâm nhập, nguy hiêm!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
