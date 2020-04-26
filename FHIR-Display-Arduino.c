#include <LiquidCrystal.h>
#include <SPI.h>
#include <MFRC522.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
MFRC522 mfrc522(53, 30);

MFRC522::MIFARE_Key key = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff};

void setup()
{
    Serial.begin(9600);
    while (!Serial);

    SPI.begin();
    mfrc522.PCD_Init();

    lcd.begin(16, 2);
    lcd.setCursor(0, 0);
    lcd.print("!FHIR HACKATHON!");
    lcd.setCursor(0, 1);
    lcd.print("Waiting...");
}
void loop()
{
      int x;
    x = analogRead(0);
        if (x < 60) {
    Serial.println("RIGHT");
    delay(500);
    }
    else if (x < 200) {
    Serial.println("UP");
    delay(500);
    }
    else if (x < 400){
    Serial.println("DOWN");
    delay(500);
    }
    else if (x < 600){
    Serial.println("LEFT");
    delay(500);
    }
    else if (x < 800){
    Serial.println("SELECT");
    delay(500);
    }


    if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    lcd.clear();
    // read all the available characters
    int count = 0;
    while (Serial.available() > 0) {
      // display each character to the LCD
      lcd.write(Serial.read());
      count = count + 1;
      if (count == 16) {
        lcd.setCursor(0,1);
      }

    }
  }

    if (!mfrc522.PICC_IsNewCardPresent())
    {
        return;
    }

    if (!mfrc522.PICC_ReadCardSerial())
    {
        return;
    }

//    Serial.print("UID tag :");
//    String content = "";
//    for (byte i = 0; i < mfrc522.uid.size; i++)
//    {
//        content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
//        content.concat(String(mfrc522.uid.uidByte[i], HEX));
//    }

    MFRC522::StatusCode status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        Serial.println("Unknown Key");
    }
    else {
        byte buffer[18];
        byte byteCount = sizeof(buffer);
        status = mfrc522.MIFARE_Read(4, buffer, &byteCount);
        String buffer_string = "";
        for (byte i = 0; i < 16; i++)
        {
            buffer_string.concat(String(buffer[i] < 0x10 ? "0" : ""));
            buffer_string.concat(String(buffer[i], HEX));
        }
        Serial.print("PATIENT:");
        Serial.println(buffer_string);
    }

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
}