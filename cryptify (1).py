from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 500)
        self.setWindowIcon(QIcon('cryptcon.jpeg'))
        self.setWindowTitle('Cryptify - Encrypt')
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

        # Encrypt Button
        self.encrypt = QPushButton('Encrypt', self)
        self.encrypt.setFont(QFont('Times New Roman', 28))

        self.encrypt.move(520, 410)
        self.encrypt.setStyleSheet('background-color: #D5D5D5;border:5px solid #717171;border-radius:10px; padding: 10px')
        self.encrypt.adjustSize()
        self.encrypt.clicked.connect(lambda: self.encodeText())

        # text
        self.text = QTextEdit(self)
        self.text.setStyleSheet('background:white; border-radius:10px; border: 2px solid gray; font-size:28px;font-family:Times New Roman')
        self.text.move(580, 10)
        self.text.setFixedSize(400, 380)
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

    def savee(self,img):
        global o

        result=cv2.imwrite('conv.png', img)
        if result==True:
            self.msg=QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Success")
            self.msg.setText("Message encrypted successfully!")
            self.msg.exec_()
            print("Saved")
        else:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Error")
            self.msg.setText("Error encrypting the message!")
            print("error")

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

            # defining function to hide the secret message into the image

    def hide_data(self, img, secret_msg):
        # calculating the maximum bytes for encoding
        nBytes = img.shape[0] * img.shape[1] * 3 // 8
        print("Maximum Bytes for encoding:", nBytes)
        # checking whether the number of bytes for encoding is less
        # than the maximum bytes in the image
        if len(secret_msg) > nBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")
        secret_msg += '#####'  # we can utilize any string as the delimiter
        dataIndex = 0
        # converting the input data to binary format using the msg_to_bin() function
        bin_secret_msg = self.msg_to_bin(secret_msg)

        # finding the length of data that requires to be hidden
        dataLen = len(bin_secret_msg)
        for values in img:
            for pixels in values:
                # converting RGB values to binary format
                r, g, b = self.msg_to_bin(pixels)
                # modifying the LSB only if there is data remaining to store
                if dataIndex < dataLen:
                    # hiding the data into LSB of Red pixel
                    pixels[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)
                    dataIndex += 1
                if dataIndex < dataLen:
                    # hiding the data into LSB of Green pixel
                    pixels[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)
                    dataIndex += 1
                if dataIndex < dataLen:
                    # hiding the data into LSB of Blue pixel
                    pixels[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)
                    dataIndex += 1
                    # if data is encoded, break out the loop
                if dataIndex >= dataLen:
                    break

        self.savee(img)


    # defining function to encode data into Image

    def encodeText(self):
        global file1
        global text

        # img_name = input("Enter image name (with extension): ")
        # reading the input image using OpenCV-Python
        img = cv2.imread(file1)

        # printing the details of the image
        print("The shape of the image is: ",
              img.shape)  # checking the image shape to calculate the number of bytes in it
        print("The original image is as shown below: ")
        # resizing the image as per the need
        resizedImg = cv2.resize(img, (500, 500))
        # displaying the image
        # cv2.imshow(resizedImg)

        data = self.text.toPlainText()

        k = 15
        encstr = ""
        for i in data:
            if (ord(i)) >= 65 and (ord(i) <= 90):
                temp = (ord(i) + k)
                if temp > 90:
                    temp = temp % 90 + 64
                encstr = encstr + chr(temp)
            elif (ord(i)) >= 97 and (ord(i) <= 122):
                temp = (ord(i) + k)
                if temp > 122:
                    temp = temp % 122 + 96
                encstr = encstr + chr(temp)
            else:
                encstr = encstr + chr(ord(i) + k)

        # print(data)
        print("Message after encryption: ", encstr)
        if (len(data) == 0):
            raise ValueError('Data is Empty')


        file_name = 'stego.jpg'
        # calling the hide_data() function to hide the secret message into the selected image
        encodedImage = self.hide_data(img, encstr)
        cv2.imwrite(file_name, encodedImage)



app = QApplication([])
mw = MainWindow()
app.exec()
