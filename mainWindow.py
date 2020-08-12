import sys
import Const
from Process_video import process_video
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from tkinter import Tk
from tkinter import filedialog


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # initialize variables
        self.scanOption = Const.SEPARATE_OPTION
        self.sourceOption = Const.RECORD_VIDEO
        self.isStopProcess = False

        # set window properties
        self.setGeometry(400, 50, 660, 660)  # x_position, y_position, width, height
        self.setWindowTitle("LessonShot")
        self.setWindowIcon(QtGui.QIcon("Resources/board_icon.png"))

        # set board image
        self.boardImg = QtWidgets.QLabel(self)
        self.boardImg.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.boardImg.setPixmap(QtGui.QPixmap("Resources/board_img.png"))
        self.boardImg.setScaledContents(True)

        # set control frame
        self.controlFrame = QtWidgets.QFrame(self)
        self.controlFrame.setGeometry(QtCore.QRect(10, 490, 640, 160))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.controlFrame.setFont(font)
        self.controlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.scanOptionL = QtWidgets.QLabel(self.controlFrame)
        self.scanOptionL.setGeometry(QtCore.QRect(10, 10, 92, 19))
        self.scanOptionL.setText("Scan Option:")

        self.sourceOptionL = QtWidgets.QLabel(self.controlFrame)
        self.sourceOptionL.setGeometry(QtCore.QRect(10, 40, 54, 19))
        self.sourceOptionL.setText("Source Option:")
        self.sourceOptionL.adjustSize()

        self.sourceLocationL = QtWidgets.QLabel(self.controlFrame)
        self.sourceLocationL.setGeometry(QtCore.QRect(10, 70, 118, 19))
        self.sourceLocationL.setText("Source Location:")

        self.outputLocationL = QtWidgets.QLabel(self.controlFrame)
        self.outputLocationL.setGeometry(QtCore.QRect(10, 100, 119, 19))
        self.outputLocationL.setText("Output Location:")

        self.sourceTL = QtWidgets.QLineEdit(self.controlFrame)
        self.sourceTL.setGeometry(QtCore.QRect(140, 70, 400, 20))

        self.outputTL = QtWidgets.QLineEdit(self.controlFrame)
        self.outputTL.setGeometry(QtCore.QRect(140, 100, 400, 20))

        self.sourceBrowseB = QtWidgets.QPushButton(self.controlFrame)
        self.sourceBrowseB.setGeometry(QtCore.QRect(550, 70, 75, 23))
        self.sourceBrowseB.setText("Browse")
        self.sourceBrowseB.clicked.connect(self.select_file)

        self.outputBrowseB = QtWidgets.QPushButton(self.controlFrame)
        self.outputBrowseB.setGeometry(QtCore.QRect(550, 100, 75, 23))
        self.outputBrowseB.setText("Browse")
        self.outputBrowseB.clicked.connect(self.select_folder)

        self.sourceOptionCB = QtWidgets.QComboBox(self.controlFrame)
        self.sourceOptionCB.setGeometry(QtCore.QRect(140, 40, 400, 22))
        self.sourceOptionCB.setObjectName("sourceCB")
        self.sourceOptionCB.addItem("Recorde Video (.mp4/ .avi)")
        self.sourceOptionCB.addItem("Camera")
        self.sourceOptionCB.activated.connect(self.set_source_option)

        self.scanOptionCB = QtWidgets.QComboBox(self.controlFrame)
        self.scanOptionCB.setGeometry(QtCore.QRect(140, 10, 400, 22))
        self.scanOptionCB.addItem("Separate - cut image every write")
        self.scanOptionCB.addItem("Append - cut image every time the board full")
        self.scanOptionCB.activated.connect(self.set_scan_option)

        self.startB = QtWidgets.QPushButton(self.controlFrame)
        self.startB.setGeometry(QtCore.QRect(200, 125, 124, 29))
        self.startB.setText("Start Processing")
        self.startB.clicked.connect(self.start_process)

        self.stopB = QtWidgets.QPushButton(self.controlFrame)
        self.stopB.setGeometry(QtCore.QRect(335, 125, 124, 29))
        self.stopB.setText("Stop Process")
        self.stopB.clicked.connect(self.stop_process)
        self.stopB.setEnabled(False)

    def start_process(self):
        source = self.sourceTL.text()
        output_path = self.outputTL.text()
        self.stopB.setEnabled(True)
        self.startB.setEnabled(False)
        process_video(self, source, output_path, self.scanOption, self.sourceOption)
        self.isStopProcess = False
        self.stopB.setEnabled(False)
        self.startB.setEnabled(True)
        self.boardImg.setPixmap(QtGui.QPixmap("Resources/board_img.png"))

    def stop_process(self):
        self.isStopProcess = True

    def set_source_option(self):
        option = self.sourceOptionCB.currentText()

        if option.startswith("Recorde Video"):
            self.sourceOption = Const.RECORD_VIDEO
            self.sourceLocationL.setText("Source Location:")
            self.sourceLocationL.adjustSize()
            self.sourceBrowseB.setEnabled(True)

        elif option.startswith("Camera"):
            self.sourceOption = Const.CAMERA
            self.sourceLocationL.setText("Camera Number:")
            self.sourceLocationL.adjustSize()
            self.sourceBrowseB.setEnabled(False)

    def set_scan_option(self):
        option = self.scanOptionCB.currentText()

        if option.startswith("Separate"):
            self.scanOption = Const.SEPARATE_OPTION

        elif option.startswith("Append"):
            self.scanOption = Const.APPEND_OPTION

    def set_board_img(self, current_img):
        # convert and set the image
        h = current_img.shape[0]
        w = current_img.shape[1]
        q_image = QtGui.QImage(current_img.data, w, h, 3 * w, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(q_image)
        self.boardImg.setPixmap(pixmap)

    def select_file(self):
        Tk().withdraw()
        file_path = filedialog.askopenfilename()
        self.sourceTL.setText(file_path)

    def select_folder(self):
        root = Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory()
        self.outputTL.setText(folder_path)

    def source_error(self, error_string):
        self.sourceTL.setText(str(error_string))

    def output_error(self, error_string):
        self.outputTL.setText(str(error_string))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
