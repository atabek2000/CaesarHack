from PyQt5 import QtCore, QtGui, QtWidgets
import math
from string import ascii_lowercase
from collections import Counter


class Ui_MainWindow(object):
    ALPHABET = ascii_lowercase
    ALPHABET_SIZE = len(ALPHABET)
    LETTER_FREQUENCY = {'e': 12.7, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09,
                        'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23,
                        'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
                        'q': 0.10, 'z': 0.07}

    GRAPH_STYLE = 'fivethirtyeight'
    LETTERS_X = list(ascii_lowercase)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(700, 300)
        MainWindow.setFixedSize(700, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 200, 50))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 200, 50))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 200, 50))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(240, 20, 430, 50))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(240, 80, 430, 50))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(240, 140, 430, 50))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.shipher_button = QtWidgets.QPushButton(self.centralwidget)
        self.shipher_button.setGeometry(QtCore.QRect(240, 200, 75, 23))
        self.shipher_button.setObjectName("shipher_button")
        self.label_error = QtWidgets.QLabel(self.centralwidget)
        self.label_error.setGeometry(QtCore.QRect(240, 240, 45, 20))
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.shipher_button.clicked.connect(self.hack)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Исходный текст:"))
        self.label_2.setText(_translate("MainWindow", "Взломанный текст:"))
        self.label_3.setText(_translate("MainWindow", "Ключ:"))
        self.shipher_button.setText(_translate("MainWindow", "Взлом"))
        self.menu.setTitle(_translate("MainWindow", "Взлом шифра Цезаря"))
        self.menu_2.setTitle(_translate("MainWindow", "(для английского алфавита)"))

    def cipher(self, text: str, key: int, decrypt: bool) -> str:
        output = ''
        for char in text:
            if char not in self.ALPHABET:
                output += char
                continue
            index = self.ALPHABET.index(char.lower())
            if decrypt:
                new_char = self.ALPHABET[(index - key) % self.ALPHABET_SIZE]
            else:
                new_char = self.ALPHABET[(index + key) % self.ALPHABET_SIZE]
            output += new_char.upper() if char.isupper() else new_char

        return output

    def difference(self,text: str) -> float:
        counter = Counter(text)
        return sum([abs(counter.get(letter, 0) * 100 / len(text) - self.LETTER_FREQUENCY[letter]) for letter in
                    self.ALPHABET]) / self.ALPHABET_SIZE

    def break_cipher(self,cipher_text: str) -> int:
        lowest_difference = math.inf
        encryption_key = 0
        for key in range(1, self.ALPHABET_SIZE):
            current_plain_text = self.cipher(cipher_text, key, True)
            current_difference = self.difference(current_plain_text)
            if current_difference < lowest_difference:
                lowest_difference = current_difference
                encryption_key = key
        return encryption_key

    def decryptCaesar(self, ch, key):
        if ord(ch) >= 65 and ord(ch) <= 90 and ord(ch) - key % 26 < 65:
            return chr(ord(ch) - key % 26 + 26)
        elif ord(ch) >= 97 and ord(ch) <= 122 and ord(ch) - key % 26 < 97:
            return chr(ord(ch) - key % 26 + 26)
        elif ord(ch) >= 1072 and ord(ch) <= 1103 and ord(ch) - key % 32 < 1072:
            return chr(ord(ch) - key % 32 + 32)
        elif ord(ch) >= 1040 and ord(ch) <= 1071 and ord(ch) - key % 32 < 1040:
            return chr(ord(ch) - key % 32 + 32)
        elif (ord(ch) >= 65 and ord(ch) <= 90) or (ord(ch) >= 97 and ord(ch) <= 122):
            return chr(ord(ch) - key % 26)
        elif (ord(ch) >= 1072 and ord(ch) <= 1103) or (ord(ch) >= 1040 and ord(ch) <= 1071):
            return chr(ord(ch) - key % 32)
        else:
            return ch

    def hack(self):
        try:
            encText = self.textEdit.toPlainText()
            key = self.break_cipher(encText)
            decArr = []
            for i in encText:
                decArr.append(self.decryptCaesar(i, key))
            decText = ''.join(decArr)
            self.textEdit_2.setPlainText(decText)
            self.label_4.setText(str(key))
        except Exception as e:
            self.label_error.setText('Error while hacking! Please, repeat later.')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
