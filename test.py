"""Test the PyQt6 charting module."""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtGui import QBrush, QColor, QGuiApplication
from PyQt5.QtCore import Qt
import pyqtgraph as pg

#Colors
PRIMARY_COLOR = "#0F0F0F"
SECONDARY_COLOR = "#232D3F"
TERTIARY_COLOR = "#005B41"
QUATERNARY_COLOR = "#008170"


class App(QWidget):
    """Main application."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {PRIMARY_COLOR}")
        #Creamos los labels
        self.label = QLabel("SiaSat - CanSat")
        self.label.setAlignment(Qt.AlignCenter)
        #self.label.setFixedWidth(int(QGuiApplication.primaryScreen().size().width()*0.9))
        #self.label.setFixedHeight(int(QGuiApplication.primaryScreen().size().height()*0.1))
        self.label.setStyleSheet(f"font-size: 63pt;color: white;background-color: {SECONDARY_COLOR};border-radius: 30px;")
        self.label.setGeometry(1, 0, int(self.width()*0.9), int(self.height()*0.1))
        # Configura la ventana
        self.setWindowTitle("SiaSat - Sistema de análisis de satélites")
        self.resize(QGuiApplication.primaryScreen().size())
        self.setMinimumSize(1080, 720)





        # Creamos el grid
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.label, 0, 0)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()
