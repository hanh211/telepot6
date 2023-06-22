import sys
import cv2
import numpy as np
from PyQt5 import Qt
from PyQt5 import QtGui
# from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication,QMainWindow
from gui import Ui_MainWindow
from ultralytics import YOLO

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic=Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.Button_start.clicked.connect(self.start_capture_video)
        # self.uic.Button_stop.clicked.connect(self.stop_capture_video)
        self.thread={}
    # def closeEvent(self,event):
    #     self.stop_capture_video()
    # def stop_capture_video(self):
    #     self.thread[1].pause_stream()
    #     self.thread[1].stop()
    def start_capture_video(self):
        self.thread[1]=live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)
    def show_wedcam(self,cv_img):
        qt_img=self.convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)
    def convert_cv_qt(self,cv_img):
        rgb_image=cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
        h,w,ch=rgb_image.shape
        bytes_per_line=ch*w
        convert_to_Qt_format=QtGui.QImage(rgb_image.data,w,h,bytes_per_line,QtGui.QImage.Format_RGB888)
        p=convert_to_Qt_format.scaled(800,600,Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

# def convert_cv_qt(self,cv_img):
#     rgb_image=cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
#     h,w,ch=rgb_image.shape
#     bytes_per_line=ch*w
#     convert_to_Qt_format=QtGui.QImage(rgb_image.data,w,h,bytes_per_line,QtGui.QImage.Format_RGB888)
#     p=convert_to_Qt_format.scaled(800,600,Qt.KeepAspectRatio)
#     return QPixmap.fromImage(p)

class live_stream(QThread):
    signal=pyqtSignal(np.ndarray)
    def __init__(self,index):
        self.index=index
        print("start",self.index)
        super(live_stream,self).__init__()
    def run(self):
        model = YOLO("yolov8n.pt")
        results = model("rtsp://admin:admin1234@ngduchanh.ddns.net:554/cam/realmonitor?channel=1&subtype=0",stream=True,show=True)
        # def show_frame():
        #     cv2.rectangle(frame,(0,0),(800,500),(255,0,0),10)
        #     cv2.imshow("show",frame)
        #     cv2.waitKey(1)
        for result,frame in results:
            self.signal.emit(frame)
            # show_frame()
            # boxes=result[0].boxes.numpy()
            # for box in boxes:
            #     print("class",box.cls)
            #     print("xyxy",box.xyxy)
            #     print("conf",box.conf)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main_win=MainWindow()
    main_win.show()
    sys.exit(app.exec())
