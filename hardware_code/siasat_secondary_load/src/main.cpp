#include <Arduino.h>
#include <LoRa.h>
#include <TinyGPS++.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>
#include <string.h>

//Init gps
#define LORA_SCK 18
#define LORA_CS 5
#define LORA_MISO 19
#define LORA_MOSI 23
#define LORA_RST 14
#define LORA_DI0 2
#define LORA_BAND 433E6
#define GPS_RX 16
#define GPS_TX 17
HardwareSerial neogps(1);
TinyGPSPlus gps;
String data;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  LoRa.setPins(LORA_CS, LORA_RST, LORA_DI0);
  if (!LoRa.begin(LORA_BAND)) {
    Serial.println("LoRa failed to initialize");
    //while (1);
  }

  Serial.println("LoRa Initializing OK!");
  //----------------------Setting up the GPS----------------------
  neogps.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  Serial.println("GPS Initializing OK!");

}

void loop() {
  // Read the GPS data
   boolean newData = false;
  for (unsigned long start = millis(); millis() - start < 10;)
  {
    while (neogps.available())
    {
      if (gps.encode(neogps.read()))
      {
        newData = true;
      }
    }
  }
  if(newData == true)
  {

    newData = false;
    Serial.println(gps.satellites.value());
    Serial.println(gps.location.lat(),6);
    Serial.println(gps.location.lng(),6);
    Serial.println(gps.altitude.meters());

  data = "Siasat Secondary Load: " + String(gps.satellites.value()) + " " + String(gps.location.lat(),6) + " " + String(gps.location.lng(),6) + " " + String(gps.altitude.meters());
    Serial.println(data);
    LoRa.beginPacket();
    LoRa.print(data);
    LoRa.endPacket();
    Serial.println("Packet Sent");


  }


}

// put function definitions here:
