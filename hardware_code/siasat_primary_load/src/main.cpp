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
//----------------------Defining Constants for the Sensors----------------------

Adafruit_BMP085 bmp;
Adafruit_MPU6050 mpu;
//----------------------Defining Constants for the GPS----------------------
#define GPS_RX 16
#define GPS_TX 17
HardwareSerial neogps(1);
TinyGPSPlus gps;
//----------------------Defining Constants for the LoRa----------------------



String data = "Hello World";


void setup() {

  //----------------------Setting up the Serial Communication----------------------
  Serial.begin(115200);
  Wire.begin(SDA, SCL);
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
    while (1);
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("MPU6050 Initializing OK!");
  
  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");

  }
  Serial.println("BMP280 Initializing OK!");
}
void loop() {
  // Read the Serial2 from the GPS
   boolean newData = false;
  for (unsigned long start = millis(); millis() - start < 1000;)
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
    Serial.print("Acceleration X: "); Serial.print(a.acceleration.x); Serial.print(" m/s^2");
    Serial.print("\tY: "); Serial.print(a.acceleration.y); Serial.print(" m/s^2");
    Serial.print("\tZ: "); Serial.print(a.acceleration.z); Serial.println(" m/s^2");

    Serial.print("Rotation X: "); Serial.print(g.gyro.x); Serial.print(" rad/s");
    Serial.print("\tY: "); Serial.print(g.gyro.y); Serial.print(" rad/s");
    Serial.print("\tZ: "); Serial.print(g.gyro.z); Serial.println(" rad/s");

    Serial.print("Temperature: ");
    Serial.print(temp.temperature);
    Serial.println(" degC");
  //Print bmp data
    Serial.print(F("Temperature = "));
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");

    Serial.print(F("Pressure = "));
    Serial.print(bmp.readPressure());
    Serial.println(" Pa");

    Serial.print(F("Approx altitude = "));
    Serial.print(bmp.readAltitude( )); // this should be adjusted to your local forcase
    Serial.println(" m");
    //Print GPS data

    Serial.println(gps.satellites.value());
    Serial.println(gps.location.lat(),6);
    Serial.println(gps.location.lng(),6);
    Serial.println(gps.altitude.meters());
    


    data="Lat:"+String(gps.location.lat(),6)+", Lon:"+String(gps.location.lng(),6)+", Alt:"+String(gps.altitude.meters())+", Temp"+String(bmp.readTemperature())+" , Press"+String(bmp.readPressure())+", Alt:"+String(bmp.readAltitude())+", Ax:"+String(a.acceleration.x)+", Ay:"+String(a.acceleration.y)+", Az:"+String(a.acceleration.z)+", Gx:"+String(g.gyro.x)+", Gy:"+String(g.gyro.y)+", Gz:"+String(g.gyro.z)+", Temp:"+String(temp.temperature);

    Serial.println(data);
    LoRa.beginPacket();
    LoRa.print(data);
    LoRa.endPacket();
    delay(1000);
    Serial.println("Data Sent");
  }
  
}

//----------------------End of the Code----------------------