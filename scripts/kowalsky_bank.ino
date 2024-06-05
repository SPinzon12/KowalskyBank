#include <ArduinoBLE.h>

BLEService kowalskiBankService("180A");  // UUID para el servicio
BLEUnsignedCharCharacteristic billClassifier("2A57", BLERead | BLENotify);

void setup() {
  // Configuración de los pines como salidas
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  // Inicialización de la comunicación serie
  Serial.begin(9600);

  while (!Serial)
    ;

  if (!BLE.begin()) {
    Serial.println("Failed to initialize BLE!\r\n");
    while (1)
      ;
  }

  BLE.setLocalName("Nano33_BLE");
  BLE.setAdvertisedService(kowalskiBankService);
  kowalskiBankService.addCharacteristic(billClassifier);
  BLE.addService(kowalskiBankService);

  BLE.advertise();

  Serial.println("Bluetooth device active, waiting for connections...\r\n");
  // Apagar todos los LEDs al iniciar
  turn_off_leds();
}

void loop() {
  BLEDevice central = BLE.central();
  if (central) {
    while (central.connected()) {
      // Comprobar si hay clases disponibles en el puerto serie
      if (Serial.available() > 0) {
        // Leer la cadena recibida hasta el carácter de nueva línea
        String clase = Serial.readStringUntil('\n');
        int claseInt = clase.toInt();  // Convertir el comando recibido a un número entero

        if (claseInt >= 0 && claseInt < 5) {
          turn_on_leds(claseInt);  // Encender el LED correspondiente
          Serial.println("Clase " + String(claseInt) + " recibida: LED encendido");
        } else {
          Serial.println("Clase inválida recibida");
        }
      }


      break;
    }
  }

  delay(100);
}

void turn_off_leds() {
  // Apagar todos los LEDs
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);
}

void turn_on_leds(int pred_index) {
  // Apagar todos los LEDs antes de encender los correspondientes
  turn_off_leds();
  byte byteToSend;

  // Encender el LED correspondiente basado en el índice de predicción
  switch (pred_index) {
    case 0:  // billete_10k: Red ON
      digitalWrite(LEDR, LOW);
      byteToSend = 0x03;
      billClassifier.writeValue(byteToSend);
      break;
    case 1:  // billete_20k: Green ON
      digitalWrite(LEDG, LOW);
      byteToSend = 0x04;
      billClassifier.writeValue(byteToSend);
      break;
    case 2:  // billete_2k: Blue ON
      digitalWrite(LEDB, LOW);
      byteToSend = 0x01;
      billClassifier.writeValue(byteToSend);
      break;
    case 3:  // billete_50k: Purple ON
      digitalWrite(LEDR, LOW);
      digitalWrite(LEDB, LOW);
      byteToSend = 0x05;
      billClassifier.writeValue(byteToSend);
      break;
    case 4:  // billete_5k: Yellow ON
      digitalWrite(LEDR, LOW);
      digitalWrite(LEDG, LOW);
      byteToSend = 0x02;
      billClassifier.writeValue(byteToSend);
      break;
    default:
      turn_off_leds();  // En caso de un índice no válido, apagar todos los LEDs
      break;
  }
}
