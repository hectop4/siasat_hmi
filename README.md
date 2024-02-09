# Interfaz Humano-Máquina para CanSat - Proyecto UNAM

Este repositorio contiene el código y la documentación para el desarrollo de la interfaz humano-máquina (HMI) de un CanSat para el concurso de la UNAM. El proyecto utiliza Python para el desarrollo del software, ESP32 para el control de hardware y LoRa para la comunicación inalámbrica.

## Descripción del Proyecto

El objetivo de este proyecto es desarrollar una interfaz fácil de usar que permita la interacción con el CanSat durante su despliegue y operación. La HMI proporcionará información en tiempo real sobre los datos recopilados por el CanSat y permitirá controlar sus funciones principales.

## Componentes del Proyecto

### 1. Software

El software de la interfaz humano-máquina se desarrollará principalmente en Python. Se utilizarán bibliotecas como PyQt para crear la interfaz gráfica de usuario (GUI). El código estará organizado en módulos para facilitar su mantenimiento y escalabilidad.

### 2. Hardware

El hardware principal del proyecto será el ESP32, un microcontrolador de bajo consumo y alto rendimiento que proporciona conectividad Wi-Fi y Bluetooth. El ESP32 se encargará de controlar los sensores y actuadores del CanSat, así como de gestionar la comunicación con la HMI a través de LoRa.

### 3. Comunicación Inalámbrica

Se utilizará el módulo LoRa para establecer una comunicación inalámbrica de largo alcance entre el CanSat y la estación base. Esto permitirá la transmisión de datos telemétricos y comandos de control de manera eficiente y confiable.
