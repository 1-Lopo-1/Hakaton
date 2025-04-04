from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontMetrics
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton

from work_window import WorkWindow


class Support(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Support")
        self.setFixedSize(1600, 900)

        line1 = QLabel(self)
        ico_line2 = QPixmap("png/line_grad.png")
        line1.setPixmap(ico_line2)
        line1.setScaledContents(True)
        line1.resize(self.width() - 30, 2)
        line1.move((self.width() - line1.width()) // 2, 110)

        # Картинка по центру экрана
        self.icon_center = QLabel(self)
        icon_pixmap = QPixmap("png/donation.png")  # Замени на путь к своей картинке
        self.icon_center.setPixmap(icon_pixmap)
        self.icon_center.setScaledContents(True)
        self.icon_center.resize(44, 44)  # Укажи нужный размер иконки

        self.icon_center.mousePressEvent = self.on_click

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

        self.icon_left.mousePressEvent = self.go_to_main_menu

        self.icon_left.mousePressEvent = self.go_to_main_menu

        # Вычисляем координаты
        icon_left_x = self.icon_center.x() - self.icon_left.width() - 120
        icon_left_y = self.icon_center.y()  # По той же вертикали

        self.icon_left.move(icon_left_x, icon_left_y)

        # Создаем label_convert и размещаем его под левой иконкой
        self.label_convert = QLabel("Конверт", self)
        self.label_convert.setAlignment(Qt.AlignCenter)
        self.label_convert.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
        """)
        # Размещаем label_convert под левой иконкой, добавляем отступ 10px
        self.label_convert.move(icon_left_x + (self.icon_left.width() - self.label_convert.width()) + 90 // 2,
                                icon_left_y + self.icon_left.height() + 10)  # Отступ 10px вниз

        # Новая иконка справа от центральной
        self.icon_right = QLabel(self)
        icon_right_pixmap = QPixmap("png/support.png")  # Укажи путь к иконке
        self.icon_right.setPixmap(icon_right_pixmap)
        self.icon_right.setScaledContents(True)
        self.icon_right.resize(44, 44)  # Размер иконки

        # Устанавливаем координаты (справа от центральной иконки на 120px)
        self.icon_right.move(self.icon_center.x() + self.icon_center.width() + 120, 20)

        # Текст под правой иконкой
        self.support_text = QLabel("Поддержка", self)
        self.support_text.setAlignment(Qt.AlignCenter)
        self.support_text.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                border-radius: 14px;
                padding: 5px 20px;
            }
        """)
        self.support_text.adjustSize()

        # Устанавливаем позицию текста (под правой иконкой)
        self.support_text.move(self.icon_right.x() + (self.icon_right.width() - self.support_text.width()) // 2,
                               self.icon_right.y() + self.icon_right.height() + 10)

        self.label = QLabel("Тех. поддержка", self)
        self.label.setAlignment(Qt.AlignCenter)  # Выравнивание по центру
        self.label.setStyleSheet("font-size: 36px; color: #000000;")  # Стилизация текста

        # Размещаем текстовое поле в центре окна с учетом отступов
        self.label.move(donation_x - 100, donation_y + 130)  # Перемещаем на 50 пикселей вниз от верхнего края окна

        # Получаем высоту текста с использованием шрифта
        font_metrics = QFontMetrics(self.label.font())
        label_height = font_metrics.height()

        # Создаем поле ввода с градиентной границей толщиной 3 пикселя
        self.text_field = QLineEdit(self)
        self.text_field.setGeometry(donation_x - 210, donation_y + 130 + label_height + 60, 475, 50)  # Под лейблом
        self.text_field.setStyleSheet("""
                   border: 2px solid transparent; /* Сделать границу прозрачной для фона */
                   background: #fff; /* Серый фон */
                   border-image: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF) 0 0 0 3 stretch;  # Градиент границы
                   font-size: 16px; /* Размер шрифта */
                   padding: 0px; /* Убираем отступы, чтобы ввод начинался с самого начала */
               """)

        # Устанавливаем параметры окна
        self.setGeometry(100, 100, 600, 600)  # Размеры окна
        self.setWindowTitle("Пример с градиентом и закруглением")

        self.text_field2 = QTextEdit(self)

        # Увеличиваем высоту поля в 2,5 раза (50 * 2.5 = 125)
        self.text_field2.setGeometry(donation_x - 210, donation_y + 130 + label_height + 60 + 50 + 10, 475, 125)
        self.text_field2.setStyleSheet("""
        border: 1px solid; /* Сделать границу прозрачной для фона */
        background: #fff; /* Серый фон */
        border-image: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF) 0 0 0 3 растянуть; /* Градиент границы */
        font-size: 16px; /* Размер шрифта */
        padding: 0px; /* Убираем отступы, чтобы ввод начинался с самого начала */
        """)

        # Создаем кнопку "Отправить"
        self.send_button = QPushButton('Отправить', self)
        self.send_button.setGeometry(175, 300, 250, 65)  # Размер 250x65
        self.send_button.setStyleSheet("""
                   QPushButton {
                       font-size: 16px;
                       color: white;
                       background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #72B7FF, stop:1 #CA59FF);
                       border: none;
                       border-radius: 10px;
                   }
                   QPushButton:hover {
                       background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #66A5FF, stop:1 #C34EFF);
                   }
               """)

        # Отступ в 20 от нижней части
        self.send_button.move(self.text_field2.x() + 105, self.text_field2.y() + self.text_field2.height() + 20)

    def on_click(self, event):
        # Закрыть текущее окно
        self.close()

        # Открыть окно с донатом
        from donate import Donate
        self.donate_window = Donate()
        self.donate_window.show()

    def go_to_main_menu(self):
        # Закрыть текущее окно
        from work_window import WorkWindow
        if not hasattr(self, 'window') or self.support_window is None:
            self.support_window = WorkWindow()  # Создаем объект окна поддержки
        self.support_window.show()  # Показываем окно поддержки
        self.close()
