import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QVBoxLayout, QFrame, QHBoxLayout


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
        self.label_audio.setStyleSheet("font-size: 16px; color: white;")
        self.label_audio.setGeometry(153, 5, 147, 32)

        self.mousePressEvent = self.toggle

    def toggle(self, event):
        self.state = not self.state
        self.update_buttons()
        if self.state:
            self.label_video.setStyleSheet("font-size: 16px; color: white; border-radius: 16px;")
            self.label_audio.setStyleSheet(
                "font-size: 16px; color: black; background-color: white; border-radius: 16px;")
        else:
            self.label_video.setStyleSheet(
                "font-size: 16px; color: black; background-color: white; border-radius: 16px;")
            self.label_audio.setStyleSheet("font-size: 16px; color: white; border-radius: 16px;")

    def update_buttons(self):
        formats = ["gif", "avi", "mov", "mp4", "wmv", "webm"] if not self.state else ["aac", "ogg", "flac", "mp3",
                                                                                      "alac", "pcm"]
        icons = self.parent().icons["video"] if not self.state else self.parent().icons["audio"]

        for i, button in enumerate(self.parent().buttons):
            button.setText(formats[i])
            self.parent().icon_labels[i].setPixmap(icons)


class PopupWindow(QWidget):
    """Всплывающее окно при нажатии на ComboBox"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор формата")
        self.setFixedSize(340, 475)

        layout = QVBoxLayout()
        label = QLabel("", self)

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
                        padding-left: 60px; /* Отступ для иконки */
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                        color: white;
                    }
                """

        self.buttons = []
        self.icon_labels = []  # Храним QLabel для иконок
        formats = ["gif", "avi", "mov", "mp4", "wmv", "webm"]

        for i in range(6):
            button = QPushButton(formats[i], self)
            button.setStyleSheet(button_stylesheet)

            button_layout = QHBoxLayout(button)
            button_layout.setContentsMargins(15, 0, 0, 0)
            button_layout.setAlignment(Qt.AlignLeft)

            icon_label = QLabel()
            icon_label.setPixmap(self.icons["video"])  # Начальное изображение
            icon_label.setFixedSize(34, 34)

            button_layout.addWidget(icon_label)
            button_layout.addStretch()

            button.setLayout(button_layout)

            layout.addWidget(button, alignment=Qt.AlignCenter)
            self.buttons.append(button)
            self.icon_labels.append(icon_label)  # Сохраняем ссылку на QLabel

        layout.addWidget(label)
        self.setLayout(layout)


# Храним окна, чтобы они не закрывались мгновенно
windows = []


def open_popup_window():
    """Функция для открытия нового окна при нажатии на ComboBox"""
    popup = PopupWindow()
    popup.show()
    windows.append(popup)  # Сохраняем ссылку на окно


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Простое окно на PyQt5")
window.setFixedSize(1400, 900)

# Чтение файла и сбор данных
def get_data_history_output():
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


convert_all = QPushButton("Конвертировать всё", window)

# Изменяем размер кнопки
convert_all.resize(200, 50)  # Устанавливаем размеры кнопки (ширина, высота)

# Задаем позицию кнопки
convert_all.move(100, 100)

# Задаем позицию кнопки с отступами 70px справа и 40px снизу
window_width = window.width()
window_height = window.height()

convert_all.move(window_width - convert_all.width() - 70, window_height - convert_all.height() - 40)

# Создаем текстовое поле
text_convert = QLabel("Конвертировать все файлы в", window)
text_convert.setStyleSheet("""
    QLabel {
        padding-left: 45px;
        padding-bottom: 88px;
        font-size: 18px;
        color: #333333;
    }
""")

# Прикрепляем текстовое поле к левому нижнему углу с отступами
text_convert.move(45, window_height - text_convert.height() - 88)

video_combo_box = QComboBox(window)
video_combo_box.addItem("MP4")
video_combo_box.addItem("Файл 2")
video_combo_box.addItem("Файл 3")
video_combo_box.setStyleSheet("""
    QComboBox {
        width: 316px;
        height: 42px;
        background-color: white;
        border: 1px solid;
        border-radius: 20px;
        border-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);  /* Градиентная обводка */
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

video_combo_box.move(350, window_height - text_convert.height() - 98)

video_combo_box.showPopup = open_popup_window

output_combo_box = QComboBox(window)
output_combo_box.setStyleSheet("""
    QComboBox {
        width: 316px;
        height: 42px;
        background-color: white;
        border: 1px solid;
        border-radius: 20px;
        border-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);  /* Градиентная обводка */
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

for i in get_data_history_output():
    output_combo_box.addItem(i)

output_combo_box.move(350, window_height - text_convert.height() - 38)

dir_image = QLabel(window)
icon_dir = QPixmap("png/dir.png")  # Укажите путь к вашей картинке
dir_image.setPixmap(icon_dir)
dir_image.setScaledContents(True)  # Масштабировать изображение в пределах QLabel
dir_image.resize(32, 32)  # Установите размер изображения

# Позиционируем картинку справа от combo box
dir_image.move(output_combo_box.x() + output_combo_box.width() + 250, output_combo_box.y() + 5)

start_menu = QLabel(window)
icon_menu = QPixmap("png/start_menu.png")  # Укажите путь к вашей картинке
start_menu.setPixmap(icon_menu)
start_menu.setScaledContents(True)  # Масштабировать изображение в пределах QLabel
start_menu.resize(650, 390)  # Установите размер изображения

# Позиционируем картинку справа от combo box
start_menu.move(
    (window_width - start_menu.width()) // 2,
    (window_height - start_menu.height()) // 2
)

line2 = QLabel(window)
ico_line1 = QPixmap("png/line.png")  # Укажите путь к новой картинке
line2.setPixmap(ico_line1)
line2.setScaledContents(True)  # Масштабировать изображение в пределах QLabel
line2.resize(window_width - 30, 2)  # Установите размер изображения (вы можете изменить это значение)

# Размещаем новую картинку на 200px ниже верхней части экрана
line2.move(
    (window_width - line2.width()) // 2,  # Центрируем по горизонтали
    120  # Вертикальное смещение на 200px ниже верхней границы
)

line1 = QLabel(window)
ico_line2 = QPixmap("png/line_grad.png")  # Укажите путь к новой картинке
line1.setPixmap(ico_line2)
line1.setScaledContents(True)  # Масштабировать изображение в пределах QLabel
line1.resize(window_width - 30, 2)  # Установите размер изображения (вы можете изменить это значение)

# Размещаем новую картинку на 200px ниже верхней части экрана
line1.move(
    (window_width - line1.width()) // 2,  # Центрируем по горизонтали
    50  # Вертикальное смещение на 200px ниже верхней границы
)


output_text = QLabel("Вывод", window)
output_text.setStyleSheet("""
    QLabel {
        padding-left: 90px;
        padding-bottom: 31px;
        font-size: 18px;
        color: #333333;
    }
""")

output_text.move(185, window_height - output_text.height() - 31)

convert_all.setStyleSheet("""
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
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #CA59FF, stop:1 #72B7FF);  /* Цвет при нажатии */
        padding: 12px;  /* Увеличиваем отступы при нажатии */
        transform: scale(0.95);  /* Немного сжимаем кнопку при нажатии */
    }
""")

# Показываем окно
window.show()

# Запускаем приложение
sys.exit(app.exec_())