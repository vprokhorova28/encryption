from pathlib import Path

from PyQt6.QtWidgets import QTextEdit, QFileDialog, QWidget, QPushButton, \
    QVBoxLayout, QHBoxLayout, QApplication, QLabel, QMainWindow, QTabWidget, \
    QGridLayout, QRadioButton, QButtonGroup, QLineEdit, QMessageBox

import encryption
import steganography

MAIN_WINDOW_LENGTH = 800
MAIN_WINDOW_WIDTH = 600


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.cipher_type = 'caesar'
        self.mode = 'encrypt'

        self.steganography_new_file_name_line_edit = None
        self.steganography_output_text_edit = None
        self.steganography_encoding_line_edit = None
        self.steganography_input_text_edit = None
        self.hack_new_file_name_line_edit = None
        self.hack_output_text_edit = None
        self.hack_encoding_line_edit = None
        self.hack_input_text_edit = None
        self.new_file_name_line_edit = None
        self.bmp_input_text_edit = None

        self.input_key_text_edit = None
        self.encoding_line_edit = None

        self.output_text_edit = None
        self.input_text_edit = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Encryption")
        self.setFixedSize(MAIN_WINDOW_LENGTH, MAIN_WINDOW_WIDTH)

        widget = QWidget()

        main_layout = QGridLayout(self)

        tab = QTabWidget(self)

        # encrypt/decrypt page
        encrypt_page = QWidget(self)
        encrypt_layout = QVBoxLayout()

        radio_btn_layout = QHBoxLayout()
        encrypt_radio_btn_layout = QVBoxLayout()
        cipher_type_radio_btn_layout = QVBoxLayout()
        radio_btn_layout.addLayout(encrypt_radio_btn_layout)
        radio_btn_layout.addLayout(cipher_type_radio_btn_layout)

        encrypt_radio_btn_group = QButtonGroup(encrypt_page)
        cipher_type_radio_btn_group = QButtonGroup(encrypt_page)

        encrypt_radio_btn = QRadioButton("Зашифровать")
        encrypt_radio_btn.setChecked(True)
        encrypt_radio_btn.action = "encrypt"
        encrypt_radio_btn.toggled.connect(lambda: self.modeRadioBtnClicked(encrypt_radio_btn))
        encrypt_radio_btn_group.addButton(encrypt_radio_btn)

        decrypt_radio_btn = QRadioButton("Расшифорвать")
        decrypt_radio_btn.action = "decrypt"
        decrypt_radio_btn.toggled.connect(lambda: self.modeRadioBtnClicked(decrypt_radio_btn))
        encrypt_radio_btn_group.addButton(decrypt_radio_btn)

        caesar_radio_btn = QRadioButton("Шифр Цезаря")
        caesar_radio_btn.setChecked(True)
        caesar_radio_btn.type = "caesar"
        caesar_radio_btn.toggled.connect(lambda: self.cipherRadioBtnClicked(caesar_radio_btn))
        cipher_type_radio_btn_group.addButton(caesar_radio_btn)

        vigener_radio_btn = QRadioButton("Шифр Виженера")
        vigener_radio_btn.type = "vigener"
        vigener_radio_btn.toggled.connect(lambda: self.cipherRadioBtnClicked(vigener_radio_btn))
        cipher_type_radio_btn_group.addButton(vigener_radio_btn)

        mode_info_label = QLabel()
        mode_info_label.setText("Выбрать режим:")
        encrypt_radio_btn_layout.addWidget(mode_info_label)
        encrypt_radio_btn_layout.addWidget(encrypt_radio_btn)
        encrypt_radio_btn_layout.addWidget(decrypt_radio_btn)

        cipher_type_info_label = QLabel()
        cipher_type_info_label.setText("Выбрать шифр:")
        cipher_type_radio_btn_layout.addWidget(cipher_type_info_label)
        cipher_type_radio_btn_layout.addWidget(caesar_radio_btn)
        cipher_type_radio_btn_layout.addWidget(vigener_radio_btn)

        encrypt_layout.addLayout(radio_btn_layout)

        key_info_label = QLabel()
        key_info_label.setText("Ключ (число для шифра Цезаря, последовательность русских букв для шифра Виженера):")
        encrypt_layout.addWidget(key_info_label)

        self.input_key_text_edit = QLineEdit()
        encrypt_layout.addWidget(self.input_key_text_edit)

        input_info_label = QLabel()
        input_info_label.setText("Путь к файлу для шифрования:")
        encrypt_layout.addWidget(input_info_label)

        input_files_layout = QHBoxLayout()
        encrypt_layout.addLayout(input_files_layout)

        self.input_text_edit = QTextEdit()
        self.input_text_edit.setReadOnly(True)
        input_files_layout.addWidget(self.input_text_edit)

        btn_layout = QVBoxLayout()
        input_files_layout.addLayout(btn_layout)

        add_file_btn = QPushButton("Выбрать файл")
        add_file_btn.clicked.connect(lambda: self.addFileBtnClicked(self.input_text_edit, 'txt'))
        btn_layout.addWidget(add_file_btn)

        delete_file_btn = QPushButton("Убрать файл")
        delete_file_btn.clicked.connect(lambda: self.deleteFileBtnClicked(self.input_text_edit))
        btn_layout.addWidget(delete_file_btn)

        encoding_info_label = QLabel()
        encoding_info_label.setText("Кодировка исходного файла:")
        encrypt_layout.addWidget(encoding_info_label)

        self.encoding_line_edit = QLineEdit("utf-8")
        encrypt_layout.addWidget(self.encoding_line_edit)

        output_info_label = QLabel()
        output_info_label.setText("Куда положить новый файл:")
        encrypt_layout.addWidget(output_info_label)

        output_files_layout = QHBoxLayout()
        encrypt_layout.addLayout(output_files_layout)

        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)
        output_files_layout.addWidget(self.output_text_edit)

        choose_dir_btn = QPushButton("Обзор")
        choose_dir_btn.clicked.connect(lambda: self.addDirBtnClicked(self.output_text_edit))
        output_files_layout.addWidget(choose_dir_btn)

        new_file_name_info_label = QLabel()
        new_file_name_info_label.setText("Как назвать новый файл (в формате ***.txt):")
        encrypt_layout.addWidget(new_file_name_info_label)

        self.new_file_name_line_edit = QLineEdit()
        encrypt_layout.addWidget(self.new_file_name_line_edit)

        execute_btn = QPushButton("Выполнить")
        execute_btn.clicked.connect(self.executionBtnClicked)
        encrypt_layout.addWidget(execute_btn)

        encrypt_layout.addWidget(QWidget())

        encrypt_page.setLayout(encrypt_layout)
        self.setCentralWidget(encrypt_page)

        tab.addTab(encrypt_page, 'Шифрование/расшифровка')

        # hack page
        hack_page = QWidget(self)
        hack_layout = QVBoxLayout()
        hack_input_info_label = QLabel()
        hack_input_info_label.setText("Путь к файлу для шифрования:")
        hack_layout.addWidget(hack_input_info_label)

        hack_input_files_layout = QHBoxLayout()
        hack_layout.addLayout(hack_input_files_layout)

        self.hack_input_text_edit = QTextEdit()
        self.hack_input_text_edit.setReadOnly(True)
        hack_input_files_layout.addWidget(self.hack_input_text_edit)

        hack_btn_layout = QVBoxLayout()
        hack_input_files_layout.addLayout(hack_btn_layout)

        hack_add_file_btn = QPushButton("Выбрать файл")
        hack_add_file_btn.clicked.connect(lambda: self.addFileBtnClicked(self.hack_input_text_edit, 'txt'))
        hack_btn_layout.addWidget(hack_add_file_btn)

        hack_delete_file_btn = QPushButton("Убрать файл")
        hack_delete_file_btn.clicked.connect(lambda: self.deleteFileBtnClicked(self.hack_input_text_edit))
        hack_btn_layout.addWidget(hack_delete_file_btn)

        encoding_info_label = QLabel()
        encoding_info_label.setText("Кодировка исходного файла:")
        hack_layout.addWidget(encoding_info_label)

        self.hack_encoding_line_edit = QLineEdit("utf-8")
        hack_layout.addWidget(self.hack_encoding_line_edit)

        output_info_label = QLabel()
        output_info_label.setText("Куда положить новый файл:")
        hack_layout.addWidget(output_info_label)

        hack_output_files_layout = QHBoxLayout()
        hack_layout.addLayout(hack_output_files_layout)

        self.hack_output_text_edit = QTextEdit()
        self.hack_output_text_edit.setReadOnly(True)
        hack_output_files_layout.addWidget(self.hack_output_text_edit)

        hack_choose_dir_btn = QPushButton("Обзор")
        hack_choose_dir_btn.clicked.connect(lambda: self.addDirBtnClicked(self.hack_output_text_edit))
        hack_output_files_layout.addWidget(hack_choose_dir_btn)

        new_file_name_info_label = QLabel()
        new_file_name_info_label.setText("Как назвать новый файл (в формате ***.txt):")
        hack_layout.addWidget(new_file_name_info_label)

        self.hack_new_file_name_line_edit = QLineEdit()
        hack_layout.addWidget(self.hack_new_file_name_line_edit)

        hack_btn = QPushButton("Взломать")
        hack_btn.clicked.connect(self.hackBtnClicked)
        hack_layout.addWidget(hack_btn)

        hack_layout.addWidget(QWidget())

        hack_page.setLayout(hack_layout)

        tab.addTab(hack_page, 'Взлом')

        # steganography page
        steganography_page = QWidget(self)
        steganography_layout = QVBoxLayout()
        bmp_input_info_label = QLabel()
        bmp_input_info_label.setText("Путь к файлу для шифрования:")
        steganography_layout.addWidget(bmp_input_info_label)

        steganography_input_files_layout = QHBoxLayout()
        steganography_layout.addLayout(steganography_input_files_layout)

        self.steganography_input_text_edit = QTextEdit()
        self.steganography_input_text_edit.setReadOnly(True)
        steganography_input_files_layout.addWidget(self.steganography_input_text_edit)

        steganography_btn_layout = QVBoxLayout()
        steganography_input_files_layout.addLayout(steganography_btn_layout)

        steganography_add_file_btn = QPushButton("Выбрать файл")
        steganography_add_file_btn.clicked.connect(
            lambda: self.addFileBtnClicked(self.steganography_input_text_edit, 'txt'))
        steganography_btn_layout.addWidget(steganography_add_file_btn)

        steganography_delete_file_btn = QPushButton("Убрать файл")
        steganography_delete_file_btn.clicked.connect(
            lambda: self.deleteFileBtnClicked(self.steganography_input_text_edit))
        steganography_btn_layout.addWidget(steganography_delete_file_btn)

        encoding_info_label = QLabel()
        encoding_info_label.setText("Кодировка исходного файла:")
        steganography_layout.addWidget(encoding_info_label)

        self.steganography_encoding_line_edit = QLineEdit("utf-8")
        steganography_layout.addWidget(self.steganography_encoding_line_edit)

        bmp_info_label = QLabel()
        bmp_info_label.setText("В какой картинке зашифровать текст:")
        steganography_layout.addWidget(bmp_info_label)

        input_bmp_layout = QHBoxLayout()
        steganography_layout.addLayout(input_bmp_layout)

        self.bmp_input_text_edit = QTextEdit()
        self.bmp_input_text_edit.setReadOnly(True)
        input_bmp_layout.addWidget(self.bmp_input_text_edit)

        choose_bmp_btn = QPushButton("Обзор")
        choose_bmp_btn.clicked.connect(lambda: self.addFileBtnClicked(self.bmp_input_text_edit, 'bmp'))
        input_bmp_layout.addWidget(choose_bmp_btn)

        output_info_label = QLabel()
        output_info_label.setText("Куда положить зашифрованный файл:")
        steganography_layout.addWidget(output_info_label)

        steganography_output_files_layout = QHBoxLayout()
        steganography_layout.addLayout(steganography_output_files_layout)

        self.steganography_output_text_edit = QTextEdit()
        self.steganography_output_text_edit.setReadOnly(True)
        steganography_output_files_layout.addWidget(self.steganography_output_text_edit)

        steganography_choose_dir_btn = QPushButton("Обзор")
        steganography_choose_dir_btn.clicked.connect(
            lambda: self.addDirBtnClicked(self.steganography_output_text_edit))
        steganography_output_files_layout.addWidget(steganography_choose_dir_btn)

        new_file_name_info_label = QLabel()
        new_file_name_info_label.setText("Как назвать новый файл (в формате ***.bmp):")
        steganography_layout.addWidget(new_file_name_info_label)

        self.steganography_new_file_name_line_edit = QLineEdit()
        steganography_layout.addWidget(self.steganography_new_file_name_line_edit)

        steganography_btn = QPushButton("Зашифровать")
        steganography_btn.clicked.connect(self.steganographyBtnClicked)
        steganography_layout.addWidget(steganography_btn)

        steganography_layout.addWidget(QWidget())

        steganography_page.setLayout(steganography_layout)

        tab.addTab(steganography_page, 'Стеганография')

        # -------

        main_layout.addWidget(tab, 0, 0)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def cipherRadioBtnClicked(self, btn):
        self.cipher_type = btn.type

    def modeRadioBtnClicked(self, btn):
        self.mode = btn.action

    def showFileDialog(self, required_layout, file_extension):
        home_dir = str(Path.home())
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать текстовый файл',
                                                home_dir, f'{file_extension} files (*.{file_extension})')

        if file_name[0]:
            required_layout.setText(file_name[0])

    def chooseDirectory(self, required_layout):
        home_dir = str(Path.home())
        dir_name = QFileDialog.getExistingDirectory(self, 'Выбрать директорию', home_dir)

        if dir_name:
            required_layout.setText(dir_name)
        
    def addFileBtnClicked(self, required_layout, file_extension):
        self.showFileDialog(required_layout, file_extension)

    def addDirBtnClicked(self, required_layout):
        self.chooseDirectory(required_layout)
    
    def deleteFileBtnClicked(self, required_layout):
        required_layout.setText('')

    def executionBtnClicked(self):
        input_file_path = self.input_text_edit.toPlainText()
        output_file_path = self.output_text_edit.toPlainText()
        new_file_name = self.new_file_name_line_edit.text()
        encoding = self.encoding_line_edit.text()
        key = self.input_key_text_edit.text()
        if not (new_file_name and key and encoding and input_file_path and output_file_path):
            msg = QMessageBox()
            msg.setText("Заполните все поля")
            msg.exec()
            return
        mode = 1
        if self.mode == "decrypt":
            mode = -1
        if self.cipher_type == "caesar":
            if not key.isdigit():
                msg = QMessageBox()
                msg.setText("Ключ должен быть числом")
                msg.exec()
                return
            encryption.caesar_cipher(input_file_path,
                                     output_file_path + '/' + new_file_name,
                                     shift=int(key),
                                     encoding=encoding,
                                     mode=mode)
        if self.cipher_type == "vigener":
            if not key.isalpha():
                msg = QMessageBox()
                msg.setText("Ключ должен состоять из русских букв")
                msg.exec()
                return
            encryption.vigener_cipher(input_file_path,
                                      output_file_path + '/' + new_file_name,
                                      key=key,
                                      encoding=encoding,
                                      mode=mode)

    def hackBtnClicked(self):
        input_file_path = self.hack_input_text_edit.toPlainText()
        output_file_path = self.hack_output_text_edit.toPlainText()
        new_file_name = self.hack_new_file_name_line_edit.text()
        encoding = self.hack_encoding_line_edit.text()
        if not (new_file_name and encoding and input_file_path and output_file_path):
            msg = QMessageBox()
            msg.setText("Заполните все поля")
            msg.exec()
            return
        encryption.decipher(input_file_path,
                            output_file_path + '/' + new_file_name,
                            encoding=encoding)

    def steganographyBtnClicked(self):
        input_bmp_path = self.bmp_input_text_edit.toPlainText()
        input_file_path = self.steganography_input_text_edit.toPlainText()
        output_file_path = self.steganography_output_text_edit.toPlainText()
        new_file_name = self.steganography_new_file_name_line_edit.text()
        encoding = self.steganography_encoding_line_edit.text()
        if not (new_file_name and encoding and input_file_path and output_file_path):
            msg = QMessageBox()
            msg.setText("Заполните все поля")
            msg.exec()
            return
        steganography.encrypt_bmp(input_bmp_path,
                                  output_file_path + '/' + new_file_name,
                                  input_file_path,
                                  encoding=encoding)


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
