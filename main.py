"""Test the PyQt6 charting module."""
# Import the required libraries
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import QIODevice,QPoint,Qt,QTimer
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo
from PyQt5 import QtCore,QtWidgets
import pyqtgraph as pg
import numpy as np


#Colors
PRIMARY_COLOR = "#0F0F0F"
SECONDARY_COLOR = "#232D3F"
TERTIARY_COLOR = "#005B41"
QUATERNARY_COLOR = "#008170"
GRAPH_1 = "#00A8E8"
GRAPH_2 = "#6528F7"
GRAPH_3 = "#D7BBF5"
GRAPH_4 = "#F9DBBB"
csv_file = "data.csv"

# Create the main application
class App(QMainWindow):
    """Main application."""
    def __init__(self):
        super(App,self).__init__()
        # Configura la ventana
        loadUi("hmi.ui",self)
        self.setWindowTitle("HMI")
        
#!SI solo hay una pantalla principal comentar la seccion, de lo contrario en rect=desktop.screenGeometry(2) cambiar el 2 por el numero de pantalla que se desea usar
#!************************************************************ 
        desktop = QDesktopWidget()
        if desktop.screenCount() > 1: 
            rect = desktop.screenGeometry(2) 
            self.move(rect.topLeft()) 
        else:
            rect = desktop.screenGeometry()
            self.move(rect.topLeft())
#!***************************************************************
        
# Eliminar barra de título y opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#*Iniciamos el grip para redimensionar la ventana
        self.gripsize = 10
        self.grip= QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripsize,self.gripsize)

#Conectamos Puerto Serial
        self.serial = QSerialPort()
        self.update.clicked.connect(self.read_ports)
        self.connect.clicked.connect(self.connect_serial)
        self.baudrate = 115200

        self.serial.readyRead.connect(self.read_serial)

#Configuramos las variables para los gráficos
#TODO Escalar los valores de los charts para que se vean bien
        self.x=list(np.linspace(0,100,100))
        self.y=list(np.linspace(0,0,100))
        self.axy=list(np.linspace(0,0,100))
        self.ayy=list(np.linspace(0,0,100))
        self.azy=list(np.linspace(0,0,100))
        self.gxy=list(np.linspace(0,0,100))
        self.gyy=list(np.linspace(0,0,100))
        self.gzy=list(np.linspace(0,0,100))
        self.t=list(np.linspace(0,0,100))
        self.p=list(np.linspace(0,0,100))
        self.h=list(np.linspace(0,0,100))
#Configuramos los colores principales de las graficas
        pg.setConfigOption('background', SECONDARY_COLOR)
        pg.setConfigOption('foreground', "white")
#? Se podra simplificar el codigo de los graficos con un for loop o una funcion?
#% Plot_Giroscope
        self.plt_giroscope=pg.PlotWidget(title="Giroscope")
        self.giroscope.addWidget(self.plt_giroscope)
        self.plt_giroscope.setYRange(-12,12)
        self.plt_giroscope.setXRange(0,100)
        self.plt_giroscope.showGrid(x=False,y=True)
        self.plt_giroscope.setLabel('left', "Angle", units='°')
        self.plt_giroscope.setLabel('bottom', "Time", units='s')
        self.plt_giroscope.addLegend()
        self.plt_giroscope.setMouseEnabled(x=False,y=True)
        #// self.plt_giroscope.plot(self.x,self.y,pen=pg.mkPen(color=GRAPH_1,width=2),name="Angle X")
        #// self.plt_giroscope.plot(self.x1,self.y1,pen=pg.mkPen(color=GRAPH_2,width=2),name="Angle Y")
        #// self.plt_giroscope.plot(self.x2,self.y2,pen=pg.mkPen(color=GRAPH_3,width=2),name="Angle Z")

        
#%Plot_Accelerometer
        self.plt_accelerometer=pg.PlotWidget(title="Accelerometer")
        self.acceleration.addWidget(self.plt_accelerometer)
        self.plt_accelerometer.setYRange(-15,15)
        self.plt_accelerometer.setXRange(0,100)
        self.plt_accelerometer.showGrid(x=False,y=True)
        self.plt_accelerometer.setMouseEnabled(x=False,y=True)
        self.plt_accelerometer.setLabel('left', "Acceleration", units='g')
        self.plt_accelerometer.setLabel('bottom', "Time", units='s')
        self.plt_accelerometer.addLegend()
        #// self.plt_accelerometer.plot(self.x,self.y,pen=pg.mkPen(color=GRAPH_1,width=2),name="Acceleration X")
        #// self.plt_accelerometer.plot(self.x1,self.y1,pen=pg.mkPen(color=GRAPH_2,width=2),name="Acceleration Y")
        #// self.plt_accelerometer.plot(self.x2,self.y2,pen=pg.mkPen(color=GRAPH_3,width=2),name="Acceleration Z")
        
#%Plot height
        self.plt_height=pg.PlotWidget(title="Height")
        self.height.addWidget(self.plt_height)
        self.plt_height.setYRange(-20,2500)
        self.plt_height.setXRange(0,100)
        self.plt_height.showGrid(x=False,y=True)
        self.plt_height.setMouseEnabled(x=False,y=True)
        self.plt_height.setLabel('left', "Height", units='m')
        self.plt_height.setLabel('bottom', "Time", units='s')
        self.plt_height.addLegend()
        #// self.plt_height.plot(self.x,self.y,pen=pg.mkPen(color=GRAPH_1,width=2),name="Height")
        
#%plot pression
        self.plt_pression=pg.PlotWidget(title="Pression")
        self.pression.addWidget(self.plt_pression)
        self.plt_pression.setYRange(0,78000)
        self.plt_pression.setXRange(0,100)
        self.plt_pression.showGrid(x=False,y=True)
        self.plt_pression.setMouseEnabled(x=False,y=True)
        self.plt_pression.setLabel('left', "Pression", units='Pa')
        self.plt_pression.setLabel('bottom', "Time", units='s')
        self.plt_pression.addLegend()
        #// self.plt_pression.plot(self.x,self.y1,pen=pg.mkPen(color=GRAPH_2,width=2),name="Pression")

#%plot temperature
        self.plt_temperature=pg.PlotWidget(title="Temperature")
        self.temperature.addWidget(self.plt_temperature)
        self.plt_temperature.setYRange(-10,50)
        self.plt_temperature.setXRange(0,100)
        self.plt_temperature.showGrid(x=False,y=True)
        self.plt_temperature.setLabel('left', "Temperature", units='°C')
        self.plt_temperature.setLabel('bottom', "Time", units='s')
        self.plt_temperature.setMouseEnabled(x=False,y=True)
        self.plt_temperature.addLegend()
        #// self.plt_temperature.plot(self.x,self.y2,pen=pg.mkPen(color=GRAPH_3,width=2),name="Temperature")

#%plot speed
        self.plt_speed=pg.PlotWidget(title="Speed")
        self.speed.addWidget(self.plt_speed)
        self.plt_speed.setYRange(-180,100)
        self.plt_speed.setXRange(0,100)
        self.plt_speed.showGrid(x=False,y=True)
        self.plt_speed.setMouseEnabled(x=False,y=True)
        self.plt_speed.setLabel('left', "Speed", units='m/s')
        self.plt_speed.setLabel('bottom', "Time", units='s')
        self.plt_speed.addLegend()
        #// self.plt_speed.plot(self.x,self.y1,pen=pg.mkPen(color=GRAPH_4,width=2),name="Speed")
#*Leemos los puertos disponibles
        self.read_ports()

    def read_ports(self):
        portlist=[]
        ports=QSerialPortInfo.availablePorts()
        for port in ports:
            portlist.append(port.portName())
        self.port_list.clear()
        self.port_list.addItems(portlist)

#*Conectamos el puerto serial
    def connect_serial(self):
        self.serial.waitForReadyRead(10)
        self.port=self.port_list.currentText()
        self.baud=self.baudrate
        self.serial.setBaudRate(self.baud)
        self.serial.setPortName(self.port)
        self.serial.open(QIODevice.ReadWrite)
        
#*Leemos los datos que llegan por el puerto serial
#! Esta seccion esta en desarrollo y se debe de mejorar para poder leer y graficar todos los datos de cada grafica
    
    def read_serial(self):
        # self.x=list(np.linspace(0,100,100))
        # self.y=list(np.linspace(0,0,100))
        if not self.serial.canReadLine(): return
        rx=self.serial.readLine()
        x=str(rx,"utf-8")
        data_dict = split_data(x)
        print(data_dict)
        
        try:
            self.azy=self.azy[1:]
            self.azy.append(float(data_dict['AZ']))
            self.ayy=self.ayy[1:]
            self.ayy.append(float(data_dict['AY']))
            self.axy=self.axy[1:]
            self.axy.append(float(data_dict['Ax']))
            self.plt_accelerometer.clear()
            self.plt_accelerometer.plot(self.x,self.ayy,pen=pg.mkPen(color=GRAPH_2,width=2),name="Acc Y")
            self.plt_accelerometer.plot(self.x,self.azy,pen=pg.mkPen(color=GRAPH_1,width=2),name="Acc Z")
            self.plt_accelerometer.plot(self.x,self.axy,pen=pg.mkPen(color=GRAPH_3,width=2),name="Acc X")
        
            #Grafico de giroscopio
            self.gzy=self.gzy[1:]
            self.gzy.append(float(data_dict['GZ']))
            self.gyy=self.gyy[1:]
            self.gyy.append(float(data_dict['GY']))
            self.gxy=self.gxy[1:]
            self.gxy.append(float(data_dict['GX']))
            self.plt_giroscope.clear()
            self.plt_giroscope.plot(self.x,self.gyy,pen=pg.mkPen(color=GRAPH_2,width=2),name="Angle Y")
            self.plt_giroscope.plot(self.x,self.gzy,pen=pg.mkPen(color=GRAPH_1,width=2),name="Angle Z")
            self.plt_giroscope.plot(self.x,self.gxy,pen=pg.mkPen(color=GRAPH_3,width=2),name="Angle X")

            #Grafico temperatura
            self.t=self.t[1:]
            self.t.append(float(data_dict['T']))
            self.plt_temperature.clear()
            self.plt_temperature.plot(self.x,self.t,pen=pg.mkPen(color=GRAPH_3,width=2),name="Temperature")

            #Grafico presion
            self.p=self.p[1:]
            self.p.append(float(data_dict['P']))
            self.plt_pression.clear()
            self.plt_pression.plot(self.x,self.p,pen=pg.mkPen(color=GRAPH_2,width=2),name="Pression")
            #Grafico altura
            self.h=self.h[1:]
            self.h.append(float(data_dict['A'].split('\r')[0]))
            self.plt_height.clear()
            self.plt_height.plot(self.x,self.h,pen=pg.mkPen(color=GRAPH_1,width=2),name="Height")
            

            
        except Exception:
            self.x=list(np.linspace(0,100,100))
            self.azy=list(np.linspace(0,0,100))
            self.ayy=list(np.linspace(0,0,100))
            self.axy=list(np.linspace(0,0,100))
            self.gxy=list(np.linspace(0,0,100))
            self.gyy=list(np.linspace(0,0,100))
            self.gzy=list(np.linspace(0,0,100))
            self.t=list(np.linspace(0,0,100))
            self.p=list(np.linspace(0,0,100))
            self.h=list(np.linspace(0,0,100))
            print("Error")


#*Funciones para cerrar la ventana en Linux y windows:
#*Para el caso de windows se cierra el programa con ctrl+q
#*Para el caso de linux se cierra el programa con ctrl+esc
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier)or (event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier):
            self.close()
#Convertimos datos del puerto seria a diccionario
def split_data(date):
    #%El formato de los datos es "AX:0.00,AY:0.00,AZ:0.00,GX:0.00,GY:0.00,GZ:0.00,T:0.00,P:0.00,A:0.00\r\n"
    #*Se debe de agregar las opciones para GPS de carga primaria y secundaria.
    
    splited= {}
    for data in date.split(","):
        try:
            splited[data.split(":")[0]]=data.split(":")[1]
            file=open(csv_file,"a")
            file.write(data)  
            file.close()

        except IndexError:
            pass
    return splited

#*Iniciamos la aplicacion
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())