FHIR-Display
============

**FHIR-Display** is a handheld device for displaying patient FHIR data. The Arduino uses the LCD keypad shield to display data pushed by the python server over serial. Push button inputs are then sent back to python. It interacts with the FHIR database with [FHIR-Parser](https://pypi.org/project/FHIR-Parser/).

CAD diagrams can be found within the CAD diagrams along with a drawing (PDF) in this folder. Jumper cables are placed between the Arduino MEGA and the RFID RC522:

* GND   ->  GND
* 3.3V  ->  3.3V
* 30    ->  RST
* 50    ->  IMI
* 51    ->  MOS
* 52    ->  SCK
* 53    ->  SDA

The LCD keypad shield is aligned so the top right pin connects to 0, RX.


Required Components
-------------------
* Arduino Mega
* LCD Keypad Shield
* RFID RC522
* 7 Jumper Cables
* Base: 1.2m x 1.75mm PLA
* Lid: 0.4m x 1.75mm PLA
