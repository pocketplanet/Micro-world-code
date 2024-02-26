#include <Arduino.h>
#include <SimpleDHT.h>

#define DHT11pin  A3
#define SoilM     A0
#define SoilT     A1
#define Phpin     A2

SimpleDHT11 dht11;

float t, h;


void setup() {
  Serial.begin(9600);
  pinMode(SoilM, INPUT);
}

void loop() {
  delay(3000);

  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  
  if ((err = dht11.read(DHT11pin, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("無法從DHT模組讀取資料, err="); Serial.println(err);
    return;
  }
  
  if (Serial.available() > 0) {
    // 當串口可用時（即樹莓派發送請求時）
    String receivedData = Serial.readStringUntil('\n');
    if (receivedData.startsWith("request_data")) {
      // 如果收到的是請求數據的指令
      t = temperature;
      h = humidity;
      int SoilMe = analogRead(SoilM);
      int SoilTe = analogRead(SoilT);
      int PhV = analogRead(Phpin);

      float ASM = map(SoilMe, 0, 1023, 0, 100);
      float AST = map(SoilTe, 0, 1023, -10, 60);
      float APV = map(PhV, 0, 1023, 0, 14);

      delay(1000);


      Serial.print("airhumidity: ");
      Serial.print((int)h);
      Serial.print("% , ");
      Serial.print("airtemperature: ");
      Serial.print((int)t);
      Serial.print("℃ , ");
      Serial.print("SoilMoisture: ");
      Serial.print((int)ASM);
      Serial.print("% , ");
      Serial.print("SoilTemperature: ");
      Serial.print((int)AST);
      Serial.print("℃ , ");
      Serial.print("PH: ");
      Serial.print((int)APV);
    }
  }
}
