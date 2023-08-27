import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QGraphicsView, QGraphicsScene, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.clicked_points = []
        self.image_pixmap = None

    def init_ui(self):
        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setScene(QGraphicsScene(self))
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graphics_view.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.graphics_view)

        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        self.table_button = QPushButton('Show Points Table', self)
        self.table_button.clicked.connect(self.show_points_table)

        self.draw_button = QPushButton('Draw Points', self)
        self.draw_button.clicked.connect(self.draw_points)

        toolbar = self.addToolBar('Image Toolbar')
        toolbar.addWidget(self.load_button)
        toolbar.addWidget(self.table_button)
        toolbar.addWidget(self.draw_button)

        self.zoom_factor = 1.0

    def load_image(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_name:
            self.image_pixmap = QPixmap(file_name)
            self.graphics_view.scene().clear()
            self.graphics_view.scene().addPixmap(self.image_pixmap)
            self.graphics_view.fitInView(self.graphics_view.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.zoom_factor = 1.0

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.graphics_view.scale(zoom_in_factor, zoom_in_factor)
            self.zoom_factor *= zoom_in_factor
        else:
            self.graphics_view.scale(zoom_out_factor, zoom_out_factor)
            self.zoom_factor *= zoom_out_factor

    def on_double_click(self, event):
        if self.image_pixmap:
            image_pos = self.graphics_view.mapToScene(event.pos())
            image_coords = (int(image_pos.x()), int(image_pos.y()))

            self.clicked_points.append(image_coords)
            print("Clicked at image coordinates:", image_coords)

    def show_points_table(self):
        table_window = PointsTableWindow(self.clicked_points)
        table_window.show()

    def draw_points(self):
        if self.image_pixmap and self.clicked_points:
            pixmap_copy = self.image_pixmap.copy()

            painter = QPainter(pixmap_copy)
            painter.setPen(QColor(255, 0, 0))

            for point in self.clicked_points:
                painter.drawEllipse(point[0] - 2, point[1] - 2, 5, 5)

            painter.end()
            self.graphics_view.scene().clear()
            self.graphics_view.scene().addPixmap(pixmap_copy)

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
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
