from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 500)
        self.setWindowIcon(QIcon('cryptcon.jpg'))
        self.setWindowTitle('Cryptify - Decryption')
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap('cbg.jpg'))
        self.bg.adjustSize()
        self.setGeometry(400, 200, 1000, 500)
        # Import Button
        self.open = QPushButton('Import', self)
        self.open.setFont(QFont('Times New Roman', 28))
        self.open.setStyleSheet('background-color: #D5D5D5;border:5px solid #717171;border-radius:10px; padding: 10px')
        self.open.adjustSize()
        self.open.move(330, 410)
        self.open.clicked.connect(lambda: self.openn())
        # Decrypt Button
        self.decrypt = QPushButton('Decrypt', self)
        self.decrypt.setFont(QFont('Times New Roman', 28))

        self.decrypt.move(520, 410)
        self.decrypt.setStyleSheet('background-color: #D5D5D5;border:5px solid #717171;border-radius:10px; padding: 10px')
        self.decrypt.adjustSize()
        self.decrypt.clicked.connect(lambda: self.decodeText())
        # text
        self.text = QTextEdit(self)
        self.text.setStyleSheet('background:white; border-radius:10px; border: 2px solid gray; font-size:28px;font-family:Times New Roman')
        self.text.move(580, 10)
        self.text.setFixedSize(400, 380)
        # text
        # self.textk = QTextEdit(self)
        # self.textk.setStyleSheet('background:white; border-radius:10px; border: 2px solid gray; font-size:18px;font-family:Times New Roman')
        # self.textk.move(10, 10)
        # self.textk.setFixedSize(280, 40)
        # image
        self.imagearea = QLabel(self)
        self.imagearea.setText('Image')
        self.imagearea.setStyleSheet('background:white; border-radius:10px; border: 2px solid gray;')
        self.imagearea.move(100, 80)
        self.imagearea.setFixedSize(200, 200)
        self.show()

    def openn(self):
        global file1
        global o
        file=QFileDialog.getOpenFileName(self, "import image", 'c://', "Image files (*.jpg *.png *.jpeg)")
        file1=file[0]
        o = cv2.imread(file1)
        print(file1)
        self.imagearea.setScaledContents(True)
        self.imagearea.setPixmap(QPixmap(file[0]))
        # self.imagearea.adjustSize()



    # converting types to binary
    def msg_to_bin(self,msg):
        if type(msg) == str:
            return ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            return [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            return format(msg, "08b")
        else:
            raise TypeError("Input type not supported")


    def show_data(self, img):
        bin_data = ""
        for values in img:
            for pixels in values:
                # converting the Red, Green, Blue values into binary format
                r, g, b = self.msg_to_bin(pixels)
                # data extraction from the LSB of Red pixel
                bin_data += r[-1]
                # data extraction from the LSB of Green pixel
                bin_data += g[-1]
                # data extraction from the LSB of Blue pixel
                bin_data += b[-1]
                # split by 8-Bits
        allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]
        # converting from bits to characters
        decodedData = ""
        for bytes in allBytes:
            decodedData += chr(int(bytes, 2))
            # checking if we have reached the delimiter which is "#####"
            if decodedData[-5:] == "#####":
                break
                # print(decodedData)
        # removing the delimiter to display the actual hidden message
        return decodedData[:-5]


    def decodeText(self):
        global file1
        global text
        # self.text.setPlaceholderText("Decryption in progress....")
        img = cv2.imread(file1)  # reading the image using the imread() function
        print("The decrypted text is as follows: ")
        text1 = self.show_data(img)

        k = 15
        decstr = ""
        for i in text1:
            if ((ord(i)) >= 65) and (ord(i)) <= 90:
                decstr = decstr + chr((ord(i) - k - 65) % 26 + 65)
            elif ((ord(i)) >= 97) and (ord(i)) <= 122:
                decstr = decstr + chr((ord(i) - k - 97) % 26 + 97)
            else:
                decstr = decstr + chr(ord(i) - k)

        if decstr == "":
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Error")
            self.msg.setText("Error decrypting the message!")
            self.msg.exec_()
            print("Saved")
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Success")
            self.msg.setText("Message decrypted successfully!")
            self.msg.exec_()


        print("Extracted encrypted message: ", text1)
        self.text.setText(decstr)
        print(text1)
        print(decstr)
        return decstr




app = QApplication([])
mw = MainWindow()
app.exec()
