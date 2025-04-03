import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QVBoxLayout, QFrame, QHBoxLayout

from support import Support
from work_window import WorkWindow


class ToggleSwitchMainWin(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(305, 42)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                border-radius: 20px;
            }
        """)
        self.state = False

        # Метка для "В обработке"
        self.label_video = QLabel("В обработке", self)
        self.label_video.setAlignment(Qt.AlignCenter)
        self.label_video.setStyleSheet("font-size: 16px; color: black; background-color: white; border-radius: 16px;")
        self.label_video.setGeometry(5, 5, 147, 32)

        # Метка для "Обработанное"
        self.label_audio = QLabel("Обработанное", self)
        self.label_audio.setAlignment(Qt.AlignCenter)
        self.label_audio.setStyleSheet("font-size: 16px; color: white; background-color: transparent; border-radius: 16px;")
        self.label_audio.setGeometry(153, 5, 147, 32)

        # Переключение состояния
        self.mousePressEvent = self.toggle

    def toggle(self, event):
        self.state = not self.state  # Переключение состояния

        # Обновление стилей в зависимости от состояния
        if self.state:
            self.label_video.setStyleSheet("font-size: 16px; color: white; background-color: transparent; border-radius: 16px;")
            self.label_audio.setStyleSheet("font-size: 16px; color: black; background-color: white; border-radius: 16px;")
        else:
            self.label_video.setStyleSheet("font-size: 16px; color: black; background-color: white; border-radius: 16px;")
            self.label_audio.setStyleSheet("font-size: 16px; color: white; background-color: transparent; border-radius: 16px;")


class ToggleSwitch(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(305, 42)
        self.setStyleSheet(""" 
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                border-radius: 20px;
            }
        """)
        self.state = False

        self.label_video = QLabel("Видео", self)
        self.label_video.setAlignment(Qt.AlignCenter)
        self.label_video.setStyleSheet("font-size: 16px; color: black; background-color: white; border-radius: 16px;")
        self.label_video.setGeometry(5, 5, 147, 32)

        self.label_audio = QLabel("Аудио", self)
        self.label_audio.setAlignment(Qt.AlignCenter)
        self.label_audio.setStyleSheet("font-size: 16px; color: white; background-color: transparent; border-radius: 16px;")
        self.label_audio.setGeometry(153, 5, 147, 32)

        self.mousePressEvent = self.toggle

    def toggle(self, event):
        self.state = not self.state
        self.update_buttons()

        if self.state:
            self.label_video.setStyleSheet("font-size: 16px; color: white; background-color: transparent; border-radius: 16px;")
            self.label_audio.setStyleSheet("font-size: 16px; color: black; background-color: white; border-radius: 16px;")
        else:
            self.label_video.setStyleSheet("font-size: 16px; color: black; background-color: white; border-radius: 16px;")
            self.label_audio.setStyleSheet("font-size: 16px; color: white; background-color: transparent; border-radius: 16px;")

    def update_buttons(self):
        formats = ["gif", "avi", "mov", "mp4", "wmv", "webm"] if not self.state else ["aac", "ogg", "flac", "mp3",
                                                                                      "alac", "pcm"]
        icons = self.parent().icons["video"] if not self.state else self.parent().icons["audio"]

        for i, button in enumerate(self.parent().buttons):
            button.setText(formats[i])
            self.parent().icon_labels[i].setPixmap(icons)


class PopupWindow(QWidget):
    button_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор формата")
        self.setFixedSize(340, 475)

        layout = QVBoxLayout()

        self.toggle_switch = ToggleSwitch(self)
        layout.addWidget(self.toggle_switch, alignment=Qt.AlignCenter)

        self.icons = {
            "video": QPixmap("png/video.png"),
            "audio": QPixmap("png/audio.png")
        }

        button_stylesheet = """
                    QPushButton {
                        width: 305px;
                        height: 42px;
                        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                        border-radius: 20px;
                        background-color: transparent;
                        font-size: 18px;
                        color: #333333;
                        text-align: left;
                        padding-left: 60px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                        color: white;
                    }
                """

        self.buttons = []
        self.icon_labels = []
        formats = ["gif", "avi", "mov", "mp4", "wmv", "webm"]

        for i in range(6):
            button = QPushButton(formats[i], self)
            button.setStyleSheet(button_stylesheet)

            button_layout = QHBoxLayout(button)
            button_layout.setContentsMargins(15, 0, 0, 0)
            button_layout.setAlignment(Qt.AlignLeft)

            icon_label = QLabel()
            icon_label.setPixmap(self.icons["video"])
            icon_label.setFixedSize(34, 34)

            button_layout.addWidget(icon_label)
            button_layout.addStretch()

            button.setLayout(button_layout)

            layout.addWidget(button, alignment=Qt.AlignCenter)
            self.buttons.append(button)
            self.icon_labels.append(icon_label)

            button.clicked.connect(self.on_button_click)

        self.setLayout(layout)

    def on_button_click(self):
        button = self.sender()
        button_text = button.text()
        self.button_clicked.emit(button_text)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простое окно на PyQt5")
        self.setFixedSize(1600, 900)

        self.toggle_switch = ToggleSwitchMainWin(self)

        self.video_combo_box = QComboBox(self)
        self.video_combo_box.addItem("mp4")
        self.video_combo_box.setStyleSheet("""
            QComboBox {
                width: 316px;
                height: 42px;
                background-color: white;
                border: 1px solid;
                border-radius: 20px;
                border-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                font-size: 18px;
                color: #333333;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #72B7FF;
                selection-background-color: #72B7FF;
            }
        """)
        self.video_combo_box.move(350, self.height() - 138)
        self.video_combo_box.mousePressEvent = self.open_popup_window

        self.popup_window = None

        self.text_convert = QLabel("Конвертировать все файлы в", self)
        self.text_convert.setStyleSheet("""
            QLabel {
                padding-left: 45px;
                padding-bottom: 88px;
                font-size: 18px;
                color: #333333;
            }
        """)

        self.text_convert.move(40, self.height() - self.text_convert.height() - 100)

        # Создаем линию с изображением
        line3 = QLabel(self)
        ico_line3 = QPixmap("png/line.png")  # Указываем путь к изображению линии
        line3.setPixmap(ico_line3)
        line3.setScaledContents(True)

        # Устанавливаем размер линии с отступами
        line3.resize(self.width() - 30, 2)  # Растягиваем на весь экран с отступом 30px слева и справа

        # Размещаем линию по центру экрана с учетом отступов
        line3.move((self.width() - line3.width()) // 2, 900 - 160)

        self.output_combo_box = QComboBox(self)
        self.output_combo_box.setStyleSheet("""
            QComboBox {
                width: 316px;
                height: 42px;
                background-color: white;
                border: 1px solid;
                border-radius: 20px;
                border-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                font-size: 18px;
                color: #333333;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #72B7FF;
                selection-background-color: #72B7FF;
            }
        """)

        for item in self.get_data_history_output():
            self.output_combo_box.addItem(item)

        self.output_combo_box.move(350, self.height() - self.text_convert.height() - 38)

        dir_image = QLabel(self)
        icon_dir = QPixmap("png/dir.png")
        dir_image.setPixmap(icon_dir)
        dir_image.setScaledContents(True)
        dir_image.resize(32, 32)
        dir_image.move(self.output_combo_box.x() + self.output_combo_box.width() + 250, self.output_combo_box.y() + 5)

        start_menu = QLabel(self)
        icon_menu = QPixmap("png/start_menu.png")
        start_menu.setPixmap(icon_menu)
        start_menu.setScaledContents(True)
        start_menu.resize(650, 390)
        start_menu.move((self.width() - start_menu.width()) // 2, (self.height() - start_menu.height()) // 2)

        start_menu.mousePressEvent = self.open_new_window

        line2 = QLabel(self)
        ico_line1 = QPixmap("png/line.png")
        line2.setPixmap(ico_line1)
        line2.setScaledContents(True)
        line2.resize(self.width() - 30, 2)
        line2.move((self.width() - line2.width()) // 2, 180)

        line1 = QLabel(self)
        ico_line2 = QPixmap("png/line_grad.png")
        line1.setPixmap(ico_line2)
        line1.setScaledContents(True)
        line1.resize(self.width() - 30, 2)
        line1.move((self.width() - line1.width()) // 2, 110)

        # Картинка слева от текста "Добавить"
        self.icon_add = QLabel(self)
        icon_pixmap = QPixmap("png/plus.png")  # Замени на путь к своей картинке
        self.icon_add.setPixmap(icon_pixmap)
        self.icon_add.setScaledContents(True)
        self.icon_add.resize(20, 20)  # Размер иконки

        icon_x = 25  # Отступ слева для иконки
        icon_y = line1.y() + line1.height() + 10  # Под line1

        text_y = icon_y  # Совмещаем по вертикали

        self.icon_add.move(icon_x, text_y + 10)

        # Картинка по центру экрана
        self.icon_center = QLabel(self)
        icon_pixmap = QPixmap("png/donation.png")  # Замени на путь к своей картинке
        self.icon_center.setPixmap(icon_pixmap)
        self.icon_center.setScaledContents(True)
        self.icon_center.resize(44, 44)  # Укажи нужный размер иконки

        # Вычисляем координаты для центрирования по горизонтали
        icon_x = (self.width() - self.icon_center.width()) // 2
        icon_y = 20  # Отступ 20px от верхнего края

        self.icon_center.move(icon_x, icon_y)

        self.donation_label = QLabel("Пожертвование", self)
        self.donation_label.setAlignment(Qt.AlignCenter)
        self.donation_label.setStyleSheet("font-size: 16px; color: #333333;")

        # Вычисляем координаты для центрирования
        donation_x = (self.width() - self.donation_label.width()) // 2
        donation_y = self.icon_center.y() + self.icon_center.height()  # 10px отступ под иконкой

        self.donation_label.move(donation_x - 10, donation_y + 15)

        # Вторая иконка (слева от первой на 120px)
        self.icon_left = QLabel(self)
        self.icon_left.setPixmap(QPixmap("png/play.png"))  # Укажи путь к иконке
        self.icon_left.setScaledContents(True)
        self.icon_left.resize(44, 44)  # Размер иконки, можно изменить

        # Вычисляем координаты
        icon_left_x = self.icon_center.x() - self.icon_left.width() - 120
        icon_left_y = self.icon_center.y()  # По той же вертикали

        self.icon_left.move(icon_left_x, icon_left_y)

        self.label_convert = QLabel("Конверт", self)
        self.label_convert.setAlignment(Qt.AlignCenter)
        self.label_convert.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                border-radius: 14px;
                padding: 5px 20px;
            }
        """)

        # Новая иконка справа от центральной
        self.icon_right = QLabel(self)
        icon_right_pixmap = QPixmap("png/support.png")  # Укажи путь к иконке
        self.icon_right.setPixmap(icon_right_pixmap)
        self.icon_right.setScaledContents(True)
        self.icon_right.resize(44, 44)  # Размер иконки

        # Устанавливаем координаты (справа от центральной иконки на 120px)
        self.icon_right.move(self.icon_center.x() + self.icon_center.width() + 120, 20)

        self.icon_right.mousePressEvent = self.open_new_window_sup  # Указываем метод для обработки

        # Текст под правой иконкой
        self.support_text = QLabel("Поддержка", self)
        self.support_text.setAlignment(Qt.AlignCenter)
        self.support_text.setStyleSheet("""
            QLabel {
                font-size: 16px;
                border-radius: 16px;
                padding: 5px 15px;
            }
        """)
        self.support_text.adjustSize()

        # Устанавливаем позицию текста (под правой иконкой)
        self.support_text.move(self.icon_right.x() + (self.icon_right.width() - self.support_text.width()) // 2,
                               self.icon_right.y() + self.icon_right.height() + 10)

        # Устанавливаем координаты под иконкой
        self.label_convert.move(self.icon_left.x() - 5 + (self.icon_left.width() - self.label_convert.width()) // 2,
                                self.icon_left.y() + self.icon_left.height() + 10)  # Отступ 10px

        self.label_add = QLabel("Добавить", self)
        self.label_add.setStyleSheet("font-size: 18px; color: #333333;")
        self.label_add.move(55, line1.y() + line1.height() + 20)  # Отступ 10px под line1

        spacing = 10  # отступ между line1 и переключателем
        toggle_x = (self.width() - self.toggle_switch.width()) // 2
        toggle_y = line1.y() + line1.height() + spacing
        self.toggle_switch.move(toggle_x, toggle_y)

        self.output_text = QLabel("Вывод", self)
        self.output_text.setStyleSheet("""
            QLabel {
                padding-left: 90px;
                padding-bottom: 31px;
                font-size: 18px;
                color: #333333;
            }
        """)
        self.output_text.move(185, self.height() - self.output_text.height() - 31)

    def open_new_window(self, event):
        self.new_window = WorkWindow()  # Создаем объект нового окна
        self.new_window.show()  # Показываем новое окно
        self.close()  # Закрываем текущее окно

    def get_data_history_output(self):
        with open("history_output") as file:
            all_data_file = file.readlines()
            counter = 1
            sub_list = []
            for i in range(3):
                try:
                    sub_list.append(all_data_file[-counter].replace("\n", ""))
                    counter += 1
                except:
                    return sub_list
        with open("history_output", "w") as file:
            for i in sub_list:
                if i != sub_list[-1]:
                    file.write(i + "\n")
                else:
                    file.write(i)
        return sub_list

    def open_popup_window(self, event):
        self.popup_window = PopupWindow()
        self.popup_window.button_clicked.connect(self.update_combo_box)
        self.popup_window.show()

    def update_combo_box(self, text):
        current_index = self.video_combo_box.findText(text)
        if current_index == -1:
            self.video_combo_box.addItem(text)
        self.video_combo_box.setCurrentText(text)

    def open_new_window_sup(self, event):
        if not hasattr(self, 'support_window') or self.support_window is None:
            self.support_window = Support()  # Создаем объект окна поддержки
        self.support_window.show()  # Показываем окно поддержки
        self.close()


app = QApplication(sys.argv)
window = MainWindow()

window.show()
sys.exit(app.exec_())
