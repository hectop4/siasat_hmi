"""Test the PyQt6 charting module."""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import QIODevice, QPoint, Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np


# Colors
PRIMARY_COLOR = "#0F0F0F"
SECONDARY_COLOR = "#232D3F"
TERTIARY_COLOR = "#005B41"
QUATERNARY_COLOR = "#008170"
GRAPH_1 = "#00A8E8"
GRAPH_2 = "#6528F7"
GRAPH_3 = "#D7BBF5"
GRAPH_4 = "#F9DBBB"


class App(QMainWindow):
    """Main application."""

    def __init__(self):
        super(App, self).__init__()
        # Configura la ventana
        loadUi("hmi.ui", self)
        self.setWindowTitle("HMI")
        # Mover la ventana a la esquina de la pantalla principal
        desktop = QDesktopWidget()
        if desktop.screenCount() > 1:
            rect = desktop.screenGeometry(1)
            self.move(rect.topLeft())
        else:
            rect = desktop.screenGeometry()
            self.move(rect.topLeft())

        # Eliminar barra de título y opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # sizegGrip
        self.gripsize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripsize, self.gripsize)

        # Conectamos Puerto Seria
        self.serial = QSerialPort()
        self.update.clicked.connect(self.read_ports)
        self.connect.clicked.connect(self.connect_serial)
        self.baudrate = 115200

        self.serial.readyRead.connect(self.read_serial)

        # Configuramos el grafico
        self.x = list(np.linspace(0, 100, 100))
        self.y = list(np.random.randint(0, 100, 100))
        self.x1 = list(np.linspace(0, 100, 100))
        self.y1 = list(np.random.randint(-100, 100, 100))
        self.x2 = list(np.linspace(0, 100, 100))
        self.y2 = list(np.random.randint(-100, 0, 100))

        # Plot Settings
        pg.setConfigOption('background', SECONDARY_COLOR)
        pg.setConfigOption('foreground', "white")
        # Plot_Giroscope
        self.plt_giroscope = pg.PlotWidget(title="Giroscope")
        self.giroscope.addWidget(self.plt_giroscope)
        self.plt_giroscope.setYRange(-180, 180)
        self.plt_giroscope.setXRange(0, 100)
        self.plt_giroscope.showGrid(x=False, y=True)
        self.plt_giroscope.setLabel('left', "Angle", units='°')
        self.plt_giroscope.setLabel('bottom', "Time", units='s')
        self.plt_giroscope.addLegend()
        self.plt_giroscope.setMouseEnabled(x=True, y=False)
        self.plt_giroscope.plot(self.x, self.y, pen=pg.mkPen(
            color=GRAPH_1, width=2), name="Angle X")
        self.plt_giroscope.plot(self.x1, self.y1, pen=pg.mkPen(
            color=GRAPH_2, width=2), name="Angle Y")
        self.plt_giroscope.plot(self.x2, self.y2, pen=pg.mkPen(
            color=GRAPH_3, width=2), name="Angle Z")

        # Plot_Accelerometer
        self.plt_accelerometer = pg.PlotWidget(title="Accelerometer")
        self.acceleration.addWidget(self.plt_accelerometer)
        self.plt_accelerometer.setYRange(-180, 100)
        self.plt_accelerometer.setXRange(0, 100)
        self.plt_accelerometer.showGrid(x=False, y=True)
        self.plt_accelerometer.setMouseEnabled(x=True, y=False)
        self.plt_accelerometer.setLabel('left', "Acceleration", units='g')
        self.plt_accelerometer.setLabel('bottom', "Time", units='s')
        self.plt_accelerometer.addLegend()
        self.plt_accelerometer.plot(self.x, self.y, pen=pg.mkPen(
            color=GRAPH_1, width=2), name="Acceleration X")
        self.plt_accelerometer.plot(self.x1, self.y1, pen=pg.mkPen(
            color=GRAPH_2, width=2), name="Acceleration Y")
        self.plt_accelerometer.plot(self.x2, self.y2, pen=pg.mkPen(
            color=GRAPH_3, width=2), name="Acceleration Z")

        # Plot height
        self.plt_height = pg.PlotWidget(title="Height")
        self.height.addWidget(self.plt_height)
        self.plt_height.setYRange(-180, 100)
        self.plt_height.setXRange(0, 100)
        self.plt_height.showGrid(x=False, y=True)
        self.plt_height.setMouseEnabled(x=True, y=False)
        self.plt_height.setLabel('left', "Height", units='m')
        self.plt_height.setLabel('bottom', "Time", units='s')
        self.plt_height.addLegend()
        self.plt_height.plot(self.x, self.y, pen=pg.mkPen(
            color=GRAPH_1, width=2), name="Height")

        # plot pression
        self.plt_pression = pg.PlotWidget(title="Pression")
        self.pression.addWidget(self.plt_pression)
        self.plt_pression.setYRange(-180, 100)
        self.plt_pression.setXRange(0, 100)
        self.plt_pression.showGrid(x=False, y=True)
        self.plt_pression.setMouseEnabled(x=True, y=False)
        self.plt_pression.setLabel('left', "Pression", units='Pa')
        self.plt_pression.setLabel('bottom', "Time", units='s')
        self.plt_pression.addLegend()
        self.plt_pression.plot(self.x, self.y1, pen=pg.mkPen(
            color=GRAPH_2, width=2), name="Pression")

        # plot temperature
        self.plt_temperature = pg.PlotWidget(title="Temperature")
        self.temperature.addWidget(self.plt_temperature)
        self.plt_temperature.setYRange(-180, 100)
        self.plt_temperature.setXRange(0, 100)
        self.plt_temperature.showGrid(x=False, y=True)
        self.plt_temperature.setLabel('left', "Temperature", units='°C')
        self.plt_temperature.setLabel('bottom', "Time", units='s')
        self.plt_temperature.setMouseEnabled(x=True, y=False)
        self.plt_temperature.addLegend()
        self.plt_temperature.plot(self.x, self.y2, pen=pg.mkPen(
            color=GRAPH_3, width=2), name="Temperature")

        # plot speed
        self.plt_speed = pg.PlotWidget(title="Speed")
        self.speed.addWidget(self.plt_speed)
        self.plt_speed.setYRange(-180, 100)
        self.plt_speed.setXRange(0, 100)
        self.plt_speed.showGrid(x=False, y=True)
        self.plt_speed.setMouseEnabled(x=True, y=False)
        self.plt_speed.setLabel('left', "Speed", units='m/s')
        self.plt_speed.setLabel('bottom', "Time", units='s')
        self.plt_speed.addLegend()
        self.plt_speed.plot(self.x, self.y1, pen=pg.mkPen(
            color=GRAPH_4, width=2), name="Speed")

        self.read_ports()

    def read_ports(self):
        portlist = []
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            portlist.append(port.portName())
        self.port_list.clear()
        self.port_list.addItems(portlist)

    def connect_serial(self):
        self.serial.waitForReadyRead(10)
        self.port = self.port_list.currentText()
        self.baud = self.baudrate
        self.serial.setBaudRate(self.baud)
        self.serial.setPortName(self.port)
        self.serial.open(QIODevice.ReadWrite)

    def read_serial(self):
        if not self.serial.canReadLine():
            return
        rx = self.serial.readLine()
        print(str(rx, 'utf-8'))

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier) or (event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier):
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
