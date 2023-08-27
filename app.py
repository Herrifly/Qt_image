import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QWidget, QVBoxLayout, \
    QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gosnias')
        self.setGeometry(100, 100, 400, 300)
        self.table_window = None
        self.pixmap = None
        self.selected_points = []
        self.count_points = 0
        self.button = QPushButton('Выберите изображение', self)
        self.button.clicked.connect(self.open_image)
        self.button.setGeometry(300, 300, 200, 200)
        self.table_button = QPushButton('Show Points Table', self)
        self.table_button.clicked.connect(self.show_points_table)


        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.mouseDoubleClickEvent = self.add_point

        self.setCentralWidget(self.image_label)  # Setting the label as the central widget

        toolbar = self.addToolBar('Image Toolbar')
        toolbar.addWidget(self.button)
        toolbar.addWidget(self.table_button)
        

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_name:
            self.pixmap = QPixmap(file_name)
            self.pixmap = self.pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.adjustSize()

    def add_point(self, event):
        pixmap = self.image_label.pixmap()
        if pixmap:
            image_pos = event.pos()  # Позиция щелчка относительно QLabel
            image_size = pixmap.size()  # Размер изображения
            x_percent = image_pos.x() / image_size.width()  # Процентное соотношение координаты X
            y_percent = image_pos.y() / image_size.height()  # Процентное соотношение координаты Y

            # Вычисление координат точки на изображении
            self.count_points += 1
            image_coords = (self.count_points, int(x_percent * image_size.width()), int(y_percent * image_size.height()))

            self.selected_points.append(image_coords)
            self.draw_points()
            print("Clicked at image coordinates:", image_coords)

    def show_points_table(self):
        self.table_window = PointsTableWindow(self.selected_points)
        self.table_window.show()

    def draw_points(self):
        if self.pixmap and self.selected_points:
            pixmap_copy = self.pixmap.copy()  # Создаем копию изображения, чтобы не менять оригинал

            painter = QPainter(pixmap_copy)
            painter.setPen(QColor(255, 0, 0))  # Красный цвет для точек

            for point in self.selected_points:
                painter.drawEllipse(point[1] - 2, point[2] - 2, 5, 5)

            painter.end()
            self.image_label.setPixmap(pixmap_copy)


class PointsTableWindow(QWidget):
    def __init__(self, points_list):
        super().__init__()

        self.setWindowTitle('Points Table')
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['X', 'Y'])

        for point in points_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(str(point[1])))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(point[2])))


        layout.addWidget(self.table_widget)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
