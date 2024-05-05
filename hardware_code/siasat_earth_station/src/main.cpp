#include <Arduino.h>
#include <LoRa.h>

#define LORA_SCK 18
#define LORA_CS 5
#define LORA_MISO 19
#define LORA_MOSI 23
#define LORA_RST 14
#define LORA_DI0 2
#define LORA_BAND 433E6



void setup() {
  //Lora Receiver
  Serial.begin(115200);

LoRa.setPins(LORA_CS, LORA_RST, LORA_DI0);
  if (!LoRa.begin(LORA_BAND)) {
    Serial.println("LoRa failed to initialize");
    //while (1);
  }

  Serial.println("LoRa Initializing OK!");

  // put your setup code here, to run once:
  
}

void loop() {
  // put your main code here, to run repeatedly:
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }

    // print RSSI of packet
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());
  }
}

// put function definitions here:
 