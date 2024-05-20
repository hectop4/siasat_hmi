//----------------------Importing Libraries----------------------
#include <Arduino.h>
#include <Wire.h>
#include <LoRa.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_MPU6050.h>
#include <TinyGPS++.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>
#include <string.h>
#include <ESP32Servo.h>


//----------------------Defining Constants for the ESP32----------------------
#define SDA 21
#define SCL 22
#define LORA_SCK 18
#define LORA_CS 5
#define LORA_MISO 19
#define LORA_MOSI 23
#define LORA_RST 14
#define LORA_DI0 2
#define LORA_BAND 433E6

#define servoPin 4
//----------------------Defining Constants for the Sensors----------------------

Adafruit_BMP085 bmp;
Adafruit_MPU6050 mpu;
//----------------------Defining Constants for the GPS----------------------
#define GPS_RX 16
#define GPS_TX 17
HardwareSerial neogps(1);
TinyGPSPlus gps;
//----------------------Defining Constants for the LoRa----------------------
volatile bool packetReceived = false;
Servo servo1;

String data = "";
String newMessage = "";

int altura_init;
int altura;
bool top=false;


void onReceive(int packetSize) {
  if (packetSize == 0) return;
  packetReceived = true;
}

void handlePacket() {


 String received = "";
  while (LoRa.available()) {
    received += (char)LoRa.read();
  }

  Serial.print("Received: ");
  Serial.println(received);

   boolean newData = false;
  for (unsigned long start = millis(); millis() - start < 100;)
  {
    while (neogps.available())
    {
      if (gps.encode(neogps.read()))
      {
        newData = true;
      }
    }
  }

  //If newData is true
  if(newData == true)
  {
    
    newData = false;
    //Print mpu data
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
   

  altura = bmp.readAltitude()-altura_init;
    
    if (altura>4 && top==false){
      
      top=true;
    }
    if (top==true && altura<2){
      servo1.write(90);
    }

    


    data=",PLa:"+String(gps.location.lat(),6)+",PLo:"+String(gps.location.lng(),6)+",T:"+String(bmp.readTemperature())+",P:"+String(bmp.readPressure())+",H:"+String(bmp.readAltitude()-altura_init)+",Ax:"+String(a.acceleration.x)+",Ay:"+String(a.acceleration.y)+",Az:"+String(a.acceleration.z)+",Gx:"+String(g.gyro.x)+",Gy:"+String(g.gyro.y)+",Gz:"+String(g.gyro.z);

  
  }





  newMessage = received + data;

  Serial.print("Sending: ");
  Serial.println(newMessage);

  LoRa.end(); // Stop LoRa
  if (!LoRa.begin(437E6)) { // Cambia a la frecuencia para repetidor-receptor
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  LoRa.beginPacket();
  LoRa.print(newMessage);
  LoRa.endPacket();

  LoRa.end(); // Stop LoRa
  if (!LoRa.begin(433E6)) { // Regresa a la frecuencia para recibir
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.receive();
}



void setup() {

  //----------------------Setting up the Serial Communication----------------------
  Serial.begin(115200);
  Wire.begin(SDA, SCL);
//----------------------Setting up the Servo----------------------
  servo1.attach(servoPin);

  //----------------------Setting up the LoRa----------------------
  LoRa.setPins(LORA_CS, LORA_RST, LORA_DI0);
  if (!LoRa.begin(LORA_BAND)) {
    Serial.println("LoRa failed to initialize");
    //while (1);
  }

  Serial.println("LoRa Initializing OK!");
  //----------------------Setting up the GPS----------------------
  neogps.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  //----------------------Setting up the Sensors----------------------
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    //while (1);
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("MPU6050 Initializing OK!");
  
  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");

  }
  Serial.println("BMP280 Initializing OK!");
  //----------------------Setting up the Servo Pos----------------------
  servo1.write(0);
  altura_init = bmp.readAltitude();

    LoRa.onReceive(onReceive);
  LoRa.receive();

}
void loop() {
  
  if (packetReceived) {
    packetReceived = false;
    handlePacket();
  }



  // Agregar un pequeño delay para permitir otras operaciones
  delay(10);
  
}


//----------------------End of the Code----------------------