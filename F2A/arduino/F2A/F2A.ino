#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


#define RST_PIN         9          
#define SS_PIN          10         

MFRC522 mfrc522(SS_PIN, RST_PIN);  
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define LED_VERDE 7
#define LED_ROJO 6

void setup() {
  Serial.begin(9600);
  SPI.begin();          
  mfrc522.PCD_Init();   
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("SISTEMA F2A");
  lcd.setCursor(0, 1);
  lcd.print("Listo...");

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
}

void loop() {
 
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
 
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }


  lcd.clear();
  lcd.print("Leyendo...");


  String uidLeido = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uidLeido += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    uidLeido += String(mfrc522.uid.uidByte[i], HEX);
  }
  uidLeido.toUpperCase(); 


  Serial.println(uidLeido); 

  while (!Serial.available()) {}
  String respuesta = Serial.readStringUntil('\n');

  lcd.clear();
  lcd.setCursor(0, 0);

  if (respuesta.startsWith("OK")) {
    digitalWrite(LED_VERDE, HIGH);
    lcd.print("ACCESO CONCEDIDO");
    
    int split = respuesta.indexOf(':');
    if (split > 0) {
      lcd.setCursor(0, 1);
      lcd.print(respuesta.substring(split + 1));
    }
  } else {
    digitalWrite(LED_ROJO, HIGH);
    lcd.print("ACCESO DENEGADO");
    lcd.setCursor(0, 1);
    lcd.print("UID NO REGIST.");
  }

  delay(3000);

  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);
  mfrc522.PICC_HaltA(); 
  lcd.clear();
  lcd.print("Pase tarjeta...");
}