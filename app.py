import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QWidget, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ГОСНИИАС')
        self.setGeometry(400, 100, 800, 600)
        self.table_window = None
        self.pixmap = None
        self.selected_points = []
        self.count_points = 0

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setScene(QGraphicsScene(self))
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graphics_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graphics_view.mouseDoubleClickEvent = self.add_point

        self.setCentralWidget(self.graphics_view)

        self.button = QPushButton('Выбрать изображение', self)
        self.button.clicked.connect(self.open_image)

        self.table_button = QPushButton('Открыть таблицу с точками', self)
        self.table_button.clicked.connect(self.show_points_table)

        self.clear_button = QPushButton('Очистить точки', self)
        self.clear_button.clicked.connect(self.delete_points)

        toolbar = self.addToolBar('Инструменты')
        toolbar.addWidget(self.button)
        toolbar.addWidget(self.table_button)
        toolbar.addWidget(self.clear_button)

        self.zoom_factor = 1.0

        # Добавляем метку для отображения уровня зума
        self.zoom_label = QLabel("Zoom: 100%", self)
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.zoom_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); padding: 2px;")
        self.zoom_label.setMargin(5)
        self.statusBar().addWidget(self.zoom_label)

    def update_zoom_label(self):
        self.zoom_label.setText(f"Zoom: {int(self.zoom_factor * 100)}%")

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")

        if file_name:
            self.pixmap = QPixmap(file_name)
            self.pixmap = self.pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.graphics_view.scene().clear()
            self.graphics_view.scene().addPixmap(self.pixmap)
            self.graphics_view.fitInView(self.graphics_view.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.zoom_factor = 1.0

    def delete_points(self):
        self.selected_points.clear()
        if self.pixmap:
            self.graphics_view.scene().addPixmap(self.pixmap)

    def add_point(self, event):
        pixmap = self.pixmap
        if pixmap:
            image_pos = self.graphics_view.mapToScene(event.pos())

            # Вычисление координат точки на изображении
            self.count_points += 1
            if self.zoom_factor > 1:
                image_coords = (self.count_points, round(image_pos.x(), 1), round(image_pos.y(), 1))
            else:
                image_coords = (self.count_points, int(image_pos.x()), int(image_pos.y()))

            self.selected_points.append(image_coords)
            self.draw_points()

    def show_points_table(self):
        self.table_window = PointsTableWindow(self.selected_points)
        self.table_window.show()

    def draw_points(self):
        if self.pixmap and self.selected_points:
            pixmap_copy = self.pixmap.copy()  

            painter = QPainter(pixmap_copy)
            painter.setPen(QColor(255, 0, 0))

            for point in self.selected_points:
                scene_point = self.graphics_view.mapToScene(int(point[1]), int(point[2]))
                view_point = self.graphics_view.mapFromScene(scene_point)
                painter.drawEllipse(view_point.x() - 2, view_point.y() - 2, 4, 4)

            painter.end()

            self.graphics_view.scene().clear()
            self.graphics_view.scene().addPixmap(pixmap_copy)

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.graphics_view.scale(zoom_in_factor, zoom_in_factor)
            self.zoom_factor *= zoom_in_factor
        else:
            self.graphics_view.scale(zoom_out_factor, zoom_out_factor)
            self.zoom_factor *= zoom_out_factor

        self.update_zoom_label()


class PointsTableWindow(QWidget):
    def __init__(self, points_list):
        super().__init__()

        self.setWindowTitle('Таблица отмеченных точек')
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

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
