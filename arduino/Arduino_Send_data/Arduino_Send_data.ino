#define LED_RIGHT 8
#define LED_LEFT 9
#define LED_TAIL 10
#define LED_HEAD 11

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_LEFT, OUTPUT);
  pinMode(LED_RIGHT, OUTPUT);
  pinMode(LED_HEAD, OUTPUT);
  pinMode(LED_TAIL, OUTPUT);

  digitalWrite(LED_LEFT, HIGH);
  digitalWrite(LED_RIGHT, HIGH);
  digitalWrite(LED_HEAD, HIGH);
  digitalWrite(LED_TAIL, HIGH);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
//  Serial.write("[ARDUINO LED_HEAD:OFF LED_TAIL:OFF LED_LEFT:OFF LED_RIGHT:OFF]\n");
  if (digitalRead(LED_HEAD) == HIGH){
    Serial.write("HEAD LIGHT is turning on!\n");
  }
  delay(500);
}
