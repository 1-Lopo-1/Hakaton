import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QVBoxLayout, QFrame, QHBoxLayout, \
    QCheckBox, QProgressBar


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


class WorkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простое окно на PyQt5")
        self.setFixedSize(1600, 900)

        self.toggle_switch = ToggleSwitchMainWin(self)

        self.convert_all = QPushButton("Конвертировать всё", self)
        self.convert_all.resize(200, 50)
        self.convert_all.move(self.width() - self.convert_all.width() - 70,
                              self.height() - self.convert_all.height() - 40)

        self.convert_all.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                        border-radius: 15px;
                        font-size: 18px;
                        color: white;
                        padding: 10px;
                        border: none;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #CA59FF, stop:1 #72B7FF);
                        padding: 12px;
                        transform: scale(0.95);
                    }
                """)

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

        # Создаем линию с изображением
        line3 = QLabel(self)
        ico_line3 = QPixmap("png/line.png")  # Указываем путь к изображению линии
        line3.setPixmap(ico_line3)
        line3.setScaledContents(True)

        # Устанавливаем размер линии с отступами
        line3.resize(self.width() - 30, 2)  # Растягиваем на весь экран с отступом 30px слева и справа

        # Размещаем линию по центру экрана с учетом отступов
        line3.move((self.width() - line3.width()) // 2, 900 - 160)

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

        # Создаем чекбокс
        self.checkbox = QCheckBox("", self)
        self.checkbox.setFixedSize(50, 50)  # Немного больше, чтобы не обрезался
        self.checkbox.move(20, 300)  # Размещаем слева с отступом 250px сверху

        # Картинка справа от чекбокса с отступом 10px
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap("png/frame_video.png"))  # Указываем путь к картинке
        self.icon_label.setScaledContents(True)
        self.icon_label.setFixedSize(250, 160)  # Размер картинки
        self.icon_label.move(self.checkbox.x() + self.checkbox.width() + 10, 250)  # 10px отступ

        self.icon_label_small = QLabel(self)
        self.icon_label_small.setPixmap(QPixmap("png/frame_video.png"))  # Указываем путь к картинке
        self.icon_label_small.setScaledContents(True)
        self.icon_label_small.setFixedSize(220, 80)  # Уменьшаем в два раза
        self.icon_label_small.move(self.icon_label.x() + self.icon_label.width() + 10, 330)  # 10px отступ вправо

        # Первая иконка
        self.icon1 = QLabel(self)
        self.icon1.setPixmap(QPixmap("png/type_video.png"))  # Указываем путь к первой иконке
        self.icon1.setAlignment(Qt.AlignCenter)
        self.icon1.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon1.move(self.icon_label_small.x() + 10,
                        self.icon_label_small.y())  # Располагаем первую иконку с отступом

        # Текст для первой иконки
        self.text1 = QLabel("Тип видео", self)
        self.text1.move(self.icon1.x() + self.icon1.width() + 5, self.icon1.y() + 10)  # Текст справа от первой иконки

        # Иконка справа от текста первой иконки
        self.icon1_extra = QLabel(self)
        self.icon1_extra.setPixmap(QPixmap("png/time.png"))  # Указываем путь к дополнительной иконке
        self.icon1_extra.setAlignment(Qt.AlignCenter)
        self.icon1_extra.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon1_extra.move(self.text1.x() + self.text1.width() - 45,
                              self.text1.y() - 10)  # Смещаем на 10px вправо от текста

        # Текст для иконки, справа от time icon
        self.text1_extra = QLabel("Время видео", self)
        self.text1_extra.move(self.icon1_extra.x() + self.icon1_extra.width(),
                              self.icon1_extra.y() + 10)  # Текст справа от иконки

        # Вторая иконка
        self.icon2 = QLabel(self)
        self.icon2.setPixmap(QPixmap("png/format.png"))  # Указываем путь ко второй иконке
        self.icon2.setAlignment(Qt.AlignCenter)
        self.icon2.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon2.move(self.icon1.x(), self.icon1.y() + 25)  # Смещаем по вертикали

        # Текст для второй иконки
        self.text2 = QLabel("Формат", self)
        self.text2.move(self.icon2.x() + self.icon2.width() + 5, self.icon2.y() + 10)  # Текст справа от второй иконки

        # Иконка справа от текста второй иконки
        self.icon2_extra = QLabel(self)
        self.icon2_extra.setPixmap(QPixmap("png/size.png"))  # Указываем путь к дополнительной иконке
        self.icon2_extra.setAlignment(Qt.AlignCenter)
        self.icon2_extra.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon2_extra.move(self.text2.x() + self.text2.width() - 45,
                              self.text2.y() - 10)  # Смещаем на 10px вправо от текста

        # Текст для иконки, справа от size icon
        self.text2_extra = QLabel("Размер", self)
        self.text2_extra.move(self.icon2_extra.x() + self.icon2_extra.width(),
                              self.icon2_extra.y() + 10)  # Текст справа от иконки

        # Третья иконка
        self.icon3 = QLabel(self)
        self.icon3.setPixmap(QPixmap("png/codec.png"))  # Указываем путь к третьей иконке
        self.icon3.setAlignment(Qt.AlignCenter)
        self.icon3.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon3.move(self.icon2.x(), self.icon2.y() + 25)

        # Текст для третьей иконки
        self.text3 = QLabel("Кодек", self)
        self.text3.move(self.icon3.x() + self.icon3.width() + 5, self.icon3.y() + 10)  # Текст справа от третьей иконки

        self.icon_label_small.setStyleSheet("""
            QLabel {
                border: 2px solid;
                border-radius: 10px;
                border-image: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
            }
        """)

        # Создаем прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # Диапазон от 0 до 100
        self.progress_bar.setValue(50)  # Устанавливаем текущий прогресс на 50%
        self.progress_bar.setGeometry(self.icon_label_small.x() + self.icon_label_small.width() + 60,
                                      self.icon_label_small.y() + 50, 200, 16)  # Устанавливаем прогресс-бар справа от контейнера

        # Устанавливаем стиль прогресс-бара
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;  /* Закругляем края прогресс-бара */
                background-color: #D9D9D9;  /* Основа прогресс-бара */
                height: 20px;  /* Устанавливаем высоту прогресс-бара */
                text-align: center;  /* Центрируем текст внутри прогресс-бара */
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #72B7FF, stop:1 #CA59FF); /* Градиентное заполнение */
                border-radius: 8px;  /* Закругляем края заполнения */
            }
            QProgressBar::text {
                color: black;
                font-size: 12px;
                font-weight: bold;
            }
        """)

        # Создаем иконку над прогресс-баром
        self.icon_progress = QLabel(self)
        self.icon_progress.setPixmap(QPixmap("png/progress.png"))  # Указываем путь к вашей иконке
        self.icon_progress.setScaledContents(True)
        self.icon_progress.setFixedSize(100, 100)  # Размер иконки
        self.icon_progress.move(self.progress_bar.x() + (self.progress_bar.width() - 90) // 2,
                                self.progress_bar.y() - 100)  # Размещаем иконку над прогресс-баром

        self.icon_label_right = QLabel(self)
        self.icon_label_right.setPixmap(QPixmap("png/frame_video.png"))  # Указываем путь к картинке
        self.icon_label_right.setScaledContents(True)
        self.icon_label_right.setFixedSize(250, 160)  # Уменьшаем в два раза
        self.icon_label_right.move(self.progress_bar.x() + self.progress_bar.width() + 60,
                                   250)  # 60px отступ вправо от прогресс-бара

        # Создаем второй контейнер размером в половину
        self.icon_label_half_right = QLabel(self)
        self.icon_label_half_right.setPixmap(QPixmap("png/frame_video.png"))  # Указываем путь к картинке
        self.icon_label_half_right.setScaledContents(True)
        self.icon_label_half_right.setFixedSize(220, 80)  # Размер в два раза меньше
        self.icon_label_half_right.move(self.icon_label_right.x() + self.icon_label_right.width() + 10,
                                        330)  # 10px отступ вправо

        # Первая иконка (справа)
        self.icon1_half_right = QLabel(self)
        self.icon1_half_right.setPixmap(QPixmap("png/type_video.png"))  # Указываем путь к первой иконке
        self.icon1_half_right.setAlignment(Qt.AlignCenter)
        self.icon1_half_right.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon1_half_right.move(self.icon_label_half_right.x() + 10,
                                   self.icon_label_half_right.y())  # Располагаем первую иконку с отступом

        # Текст для первой иконки (справа)
        self.text1_half_right = QLabel("Тип видео", self)
        self.text1_half_right.move(self.icon1_half_right.x() + self.icon1_half_right.width() + 5,
                                   self.icon1_half_right.y() + 10)  # Текст справа от первой иконки

        # Иконка справа от текста первой иконки
        self.icon1_extra_half_right = QLabel(self)
        self.icon1_extra_half_right.setPixmap(QPixmap("png/time.png"))  # Указываем путь к дополнительной иконке
        self.icon1_extra_half_right.setAlignment(Qt.AlignCenter)
        self.icon1_extra_half_right.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon1_extra_half_right.move(self.text1_half_right.x() + self.text1_half_right.width() - 45,
                                         self.text1_half_right.y() - 10)  # Смещаем на 10px вправо от текста

        # Текст для иконки, справа от time icon
        self.text1_extra_half_right = QLabel("Время видео", self)
        self.text1_extra_half_right.move(self.icon1_extra_half_right.x() + self.icon1_extra_half_right.width(),
                                         self.icon1_extra_half_right.y() + 10)  # Текст справа от иконки

        # Вторая иконка (справа)
        self.icon2_half_right = QLabel(self)
        self.icon2_half_right.setPixmap(QPixmap("png/format.png"))  # Указываем путь ко второй иконке
        self.icon2_half_right.setAlignment(Qt.AlignCenter)
        self.icon2_half_right.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon2_half_right.move(self.icon1_half_right.x(), self.icon1_half_right.y() + 25)  # Смещаем по вертикали

        # Текст для второй иконки (справа)
        self.text2_half_right = QLabel("Формат", self)
        self.text2_half_right.move(self.icon2_half_right.x() + self.icon2_half_right.width() + 5,
                                   self.icon2_half_right.y() + 10)  # Текст справа от второй иконки

        # Иконка справа от текста второй иконки
        self.icon2_extra_half_right = QLabel(self)
        self.icon2_extra_half_right.setPixmap(QPixmap("png/size.png"))  # Указываем путь к дополнительной иконке
        self.icon2_extra_half_right.setAlignment(Qt.AlignCenter)
        self.icon2_extra_half_right.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon2_extra_half_right.move(self.text2_half_right.x() + self.text2_half_right.width() - 45,
                                         self.text2_half_right.y() - 10)  # Смещаем на 10px вправо от текста

        # Текст для иконки, справа от size icon
        self.text2_extra_half_right = QLabel("Размер", self)
        self.text2_extra_half_right.move(self.icon2_extra_half_right.x() + self.icon2_extra_half_right.width(),
                                         self.icon2_extra_half_right.y() + 10)  # Текст справа от иконки

        # Третья иконка (справа)
        self.icon3_half_right = QLabel(self)
        self.icon3_half_right.setPixmap(QPixmap("png/codec.png"))  # Указываем путь к третьей иконке
        self.icon3_half_right.setAlignment(Qt.AlignCenter)
        self.icon3_half_right.setFixedSize(32, 32)  # Устанавливаем размер иконки
        self.icon3_half_right.move(self.icon2_half_right.x(), self.icon2_half_right.y() + 25)

        # Текст для третьей иконки (справа)
        self.text3_half_right = QLabel("Кодек", self)
        self.text3_half_right.move(self.icon3_half_right.x() + self.icon3_half_right.width() + 5,
                                   self.icon3_half_right.y() + 10)  # Текст справа от третьей иконки

        # Стиль для маленького контейнера с иконками и текстами (переименованный)
        self.icon_label_half_right.setStyleSheet("""
            QLabel {
                border: 2px solid;
                border-radius: 10px;
                border-image: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
            }
        """)

        # Стиль чекбокса: прозрачный фон вокруг, градиент
        self.checkbox.setStyleSheet("""
                    QCheckBox {
                        spacing: 5px; /* Отступы внутри */
                    }
                    QCheckBox::indicator {
                        width: 40px;
                        height: 40px;
                        border-radius: 20px;
                        background: white;
                        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                        margin: 5px; /* Убирает обрезание */
                    }
                    QCheckBox::indicator:checked {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                    }
                """)

        # Устанавливаем координаты (справа от центральной иконки на 120px)
        self.icon_right.move(self.icon_center.x() + self.icon_center.width() + 120, 20)

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

