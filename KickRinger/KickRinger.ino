//
//  kickringer.ino
//
//  Created by Jonathan Moyes on 11/3/13.
//  Modular Robotics 2013
//

int bell1 = 11;
int recByte;

void setup() {                
  pinMode(bell1, OUTPUT);     
  digitalWrite(bell1, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    recByte = Serial.read();
    ringBell1();
  }
}

void ringBell1(){
  digitalWrite(bell1, HIGH); // Energize the solenoid
  delay(3);                  // 3ms to close solenoid
  digitalWrite(bell1, LOW);  // De-energize the solenoid
}
