#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Dirección I2C común: 0x27. Si no funciona, prueba con 0x3F.
// Requiere instalar librería: "LiquidCrystal I2C"
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define LED_VERDE 7
#define LED_ROJO 6

String UID_SIMULADO = "UID_BLmmmANCO";  // Cambia por AZUL o BLANCO

void setup() {
  Serial.begin(9600);
  
  // INICIO LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("SISTEMA F2A");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  
  // NOTA: No enviamos prints de debug (ej. "ARDUINO_READY") por Serial
  // porque el script de Python creería que es un UID de tarjeta y daría error.
}

void loop() {
  delay(5000); // Enviamos tarjeta cada 5 segundos
  
  lcd.clear();
   lcd.print("Pase tarjeta...");
  delay(3000);
  lcd.clear();
  lcd.print("Leyendo tarjeta...");
  Serial.println(UID_SIMULADO); // ENVIA UID A PYTHON
  delay(2000);
  
  // Esperar respuesta de Python
  while (!Serial.available()) {}
  
  String respuesta = Serial.readStringUntil('\n');
  
  // NOTA: No hacemos Serial.println de lo recibido, o Python lo leerá de nuevo como tarjeta.

  lcd.clear();
  lcd.setCursor(0, 0);

  if (respuesta.startsWith("OK")) {
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_ROJO, LOW);
    
    lcd.print("ACCESO CONCEDIDO");
    
    // Mostramos mensaje extra si viene (ej. "OK:Bienvenido...")
    int split = respuesta.indexOf(':');
    if (split > 0) {
      lcd.setCursor(0, 1);
      lcd.print(respuesta.substring(split + 1));
    }
    
  } else {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_ROJO, HIGH);
    lcd.print("ACCESO DENEGADO");
  }

  delay(3000);
  
  // Reset estado
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);
  lcd.clear();
 
}
