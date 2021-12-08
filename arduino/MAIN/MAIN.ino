#include <MPU6050_tockn.h>
#include <Wire.h>

// L298N pins control motors
#define IN1  7
#define IN2 6 // PWM pin
#define IN3 5 // PWM pin
#define IN4 4
#define MAX_SPEED 255 // Max speed value of motor
#define MIN_SPEED 0 // Min speed value of motor

// LED pins
#define LED_RIGHT 8
#define LED_LEFT 9
#define LED_STOP 10
#define LED_HEAD 11

//================================================================
// GY-521 sensor setup
// SCL - A5; SDA - A4; INT - D2
MPU6050 mpu6050(Wire);

//================================================================
// Speed of 2 motors
int MOTOR_A=0;
int MOTOR_B=0;

// HEAD, LEFT, RIGHT, STOP lights
int LIGHT[4] = {0, 0, 0, 0}; // use bool instead?

// Array of status code
String SystemCode[4] = {"000", "001", "010", "011"}; // 000-welcome 001-testSystem 010-BUZZ 011-Goodbye
String SensorCode[6] = {"100", "101", "111", "120", "121", "122"};
String MotorCode[2] = {"200", "201"}; // 200-RIGHT MOTOR; 201-LEFT MOTOR
String LightCode[4] = {"300", "301", "302", "303"};
String Msg; // Message command from PC

// define functions
int welcome(); // Start car,flash light
int testSystem(); // Check all element in car
int buzz(); // control Buzz speaker
int goodbye(); // Left car, flash light

int Msg2Command(String Msg, char separator);
int excuteCommand(String Cmd, char separator);

int controlLight(); // function control lights
int controlMotor(); // function control motor speeds

void Motor_1_Stop(); // Function stop motor A
void Motor_2_Stop(); // Function stop motor B
void Motor_1_Up(int speed);
void Motor_2_Up(int speed);
void Motor_1_Back(int speed);
void Motor_2_Back(int speed);

int sendGY521(); // Send data from GY521 sensor to PC via Serial
//================================================================
void setup() {
  // Start Serial at port 9600
  Serial.begin(9600);
  
  // Set pinMode for LED pin control
  pinMode(LED_LEFT, OUTPUT);
  pinMode(LED_RIGHT, OUTPUT);
  pinMode(LED_HEAD, OUTPUT);
  pinMode(LED_STOP, OUTPUT);
  
  // Turn off all LED
  digitalWrite(LED_LEFT, LOW);
  digitalWrite(LED_RIGHT, LOW);
  digitalWrite(LED_HEAD, LOW);
  digitalWrite(LED_STOP, LOW);
  
  // Setup GY521 Sensor
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  welcome();
  Serial.write("System started!\n");
}
//================================================================
void loop() {
  // Read Msg from Serial
  if (Serial.available() > 0){
    char temp = Serial.read();
    if (temp == '\n'){
      // Extract Msg to separate commands and excute all commands
      Msg2Command(Msg, ' ');
      Msg = ""; // reset message
    }
    else { Msg += temp; }
//      Msg = Serial.readStringUntil('\n'); // don't use this solution, it make python comunity via pyserial slowly than 1-2 sec
  }
  
  // Control System
  controlLight();
  controlMotor();
  
  //Sensor GY521 Update
  mpu6050.update();
  sendGY521();
 }
 
//================================================================
int welcome(){
  for(int i=0; i<3; i++){
    digitalWrite(LED_HEAD, LOW);
    digitalWrite(LED_LEFT, HIGH);
    digitalWrite(LED_RIGHT, HIGH);
    delay(200);
    digitalWrite(LED_HEAD, HIGH);
    digitalWrite(LED_LEFT, LOW);
    digitalWrite(LED_RIGHT, LOW);
    delay(200);
  }
  digitalWrite(LED_HEAD, LOW);
  for(int i=0; i<3; i++){
    digitalWrite(LED_LEFT, HIGH);
    digitalWrite(LED_RIGHT, LOW);
    delay(200);
    digitalWrite(LED_LEFT, LOW);
    digitalWrite(LED_RIGHT, HIGH);
    delay(200);
  }
  digitalWrite(LED_LEFT, LOW);
  digitalWrite(LED_RIGHT, LOW);
  for(int i=0; i<3; i++){
    digitalWrite(LED_HEAD, HIGH);
    delay(100);
    digitalWrite(LED_HEAD, LOW);
    delay(100);
  }
  digitalWrite(LED_LEFT, HIGH);
  digitalWrite(LED_RIGHT,HIGH);
  delay(500);
  digitalWrite(LED_LEFT, LOW);
  digitalWrite(LED_RIGHT, LOW);
}
//================================================================
int testSystem(){
  digitalWrite(LED_HEAD, HIGH);
  digitalWrite(LED_STOP, HIGH);
  digitalWrite(LED_LEFT, HIGH);
  digitalWrite(LED_RIGHT, HIGH);
  delay(200);
  digitalWrite(LED_HEAD, LOW);
  digitalWrite(LED_STOP, LOW);
  digitalWrite(LED_LEFT, LOW);
  digitalWrite(LED_RIGHT, LOW);
  delay(200);
  Motor_1_Up(100);
  Motor_2_Up(100);
  delay(200);
  Motor_1_Back(100);
  Motor_2_Back(100);
  delay(200);
  Motor_1_Stop();
  Motor_2_Stop();
  delay(200); 
  return 0;
}
//================================================================
int goodbye(){
  for(int i=0; i<2; i++){
    digitalWrite(LED_HEAD, HIGH);
    delay(200);
    digitalWrite(LED_HEAD, LOW);
    delay(200);
  }
  for(int i=0; i<2; i++){
    digitalWrite(LED_LEFT, HIGH);
    digitalWrite(LED_RIGHT, HIGH);
    delay(200);
    digitalWrite(LED_LEFT, LOW);
    digitalWrite(LED_RIGHT, LOW);
    delay(200);
  }
}

//================================================================
int sendGY521(){
  Serial.print("X:");
  Serial.print(mpu6050.getAngleX());
  Serial.print(" Y:");
  Serial.print(mpu6050.getAngleY());
  Serial.print(" Z:");
  Serial.println(mpu6050.getAngleZ());
  return 0;
}

// Command: "Code:Status"
int Msg2Command(String Msg, char separator){
  int lenMsg = Msg.length()-1;
  String Cmd="";

  // Split Msg to string command
  for(int i=0; i<=lenMsg; i++){
    if (Msg[i] != separator){
      Cmd+= Msg[i];
    }
    if(Cmd.length() > 0 && (Msg[i] == separator || i == lenMsg)){
//      Serial.println(Cmd);
      executeCommand(Cmd, ':'); // Excute command
 
      Cmd = ""; // Reset to read new command
    }
  }
  return 0;
}

int executeCommand(String Cmd, char separator){
  int indexSeparator = Cmd.indexOf(separator);
  String Element = Cmd.substring(0, indexSeparator);
  int Status = Cmd.substring(indexSeparator + 1).toInt();

  // System commands
  if (Element[0] == '0'){
     if (Element == SystemCode[0]){ welcome(); }
     if (Element == SystemCode[1]){ testSystem(); }
//     if (Element == SystemCode[2]){  }
     if (Element == SystemCode[3]){ goodbye(); }
  }
  // Sensor commands
  else if (Element[0] == '1'){

  }
  // Motor commands
  else if (Element[0] == '2'){
    if (Element == MotorCode[0]){ MOTOR_A = Status; }
    if (Element == MotorCode[1]){ MOTOR_B = Status; }
  }
  // Light commands
  else if (Element[0] == '3'){
    for(int i=0; i<sizeof(LightCode);i++){
      if (Element == LightCode[i]){ LIGHT[i]=Status;}
    }
  }  
  return 0;
}

//================================================================
// Control Light
int controlLight(){
  // Control head light
  if (LIGHT[0] != 0) { digitalWrite(LED_HEAD, HIGH); }
  else { digitalWrite(LED_HEAD, LOW); }

  // Control left light
  if (LIGHT[1] != 0) { digitalWrite(LED_LEFT, HIGH); }
  else { digitalWrite(LED_LEFT, LOW); }

  // Control right light
  if (LIGHT[2] != 0) { digitalWrite(LED_RIGHT, HIGH); }
  else { digitalWrite(LED_RIGHT, LOW); }

  // Control stop light
  if (LIGHT[3] != 0) { digitalWrite(LED_STOP, HIGH); }
  else { digitalWrite(LED_STOP, LOW); }
}

// Control Motor speeds
int controlMotor(){
  // If speed value = 0: Motor stops.
  // If speed value > 0: Motor goes ahead.
  // If speed value < 0: Motor goes back.
  
  // Motor A
  if (MOTOR_A == 0){ Motor_1_Stop(); }
  else if (MOTOR_A < 0){ Motor_1_Back(abs(MOTOR_A)); }
  else { Motor_1_Up(MOTOR_A); }
  
  // Motor B
  if (MOTOR_B == 0){ Motor_2_Stop(); }
  else if (MOTOR_B < 0){ Motor_2_Back(abs(MOTOR_B)); }
  else { Motor_2_Up(MOTOR_B); }
  return 0;
}

//================================================================
// Control L298N Motor driver
// Source: http://arduino.vn/bai-viet/893-cach-dung-module-dieu-khien-dong-co-l298n-cau-h-de-dieu-khien-dong-co-dc
void Motor_1_Stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}
 
void Motor_2_Stop() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
 
void Motor_1_Up(int speed) { // 0 - MAX_SPEED
  speed = constrain(speed, MIN_SPEED, MAX_SPEED); // 0 - MAX_SPEED - http://arduino.vn/reference/constrain
  digitalWrite(IN1, HIGH);
  analogWrite(IN2, 255 - speed);
}
 
void Motor_1_Back(int speed) {
  speed = constrain(speed, MIN_SPEED, MAX_SPEED); // 0 - MAX_SPEED - http://arduino.vn/reference/constrain
  digitalWrite(IN1, LOW);
  analogWrite(IN2, speed);
}
 
void Motor_2_Up(int speed) { // 0 - MAX_SPEED
  speed = constrain(speed, MIN_SPEED, MAX_SPEED); // 0 - MAX_SPEED - http://arduino.vn/reference/constrain
  analogWrite(IN3, speed);
  digitalWrite(IN4, LOW);
}
 
void Motor_2_Back(int speed) {
  speed = constrain(speed, MIN_SPEED, MAX_SPEED); // 0 - MAX_SPEED - http://arduino.vn/reference/constrain
  analogWrite(IN3, 255 - speed);
  digitalWrite(IN4, HIGH);
}
