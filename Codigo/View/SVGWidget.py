from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtSvg import QSvgRenderer


class SVGWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.renderer = None

    def load_svg(self, svg_file_path):
        self.renderer = QSvgRenderer(svg_file_path)
        self.update()

    def paintEvent(self, event):
        if self.renderer:
            painter = QPainter(self)
            self.renderer.render(painter)
            painter.end()
