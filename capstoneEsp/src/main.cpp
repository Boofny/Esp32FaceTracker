#include <ESP32Servo.h>
#include <Arduino.h>
String inputString;

Servo left_right;
Servo up_down;

void setup()
{
  left_right.attach(19);
  up_down.attach(18);
  Serial.begin(9600);
}


void loop()
{
  while(Serial.available()) // while serial is valid read data sent from python to the port 
  {
    inputString = Serial.readStringUntil('\r'); // read each line to the new carige return 
    Serial.println(inputString); // print for debugging

    // parse the x and y from the serial port 
    int x_axis = inputString.substring(0, inputString.indexOf(',')).toInt();
    int y_axis = inputString.substring(inputString.indexOf(',') + 1).toInt();

    int y = map(y_axis, 0, 1000, 180, 0); // scale both x and y to the angle of the 180 degree servos with datas range of 0 - 1000
    int x = map(x_axis, 0, 1000, 180, 0);

    left_right.write(x);
    up_down.write(y);
    
    // Print the parsed values
    Serial.print("First Integer: ");
    Serial.println(x);
    Serial.print("Second Integer: ");
    Serial.println(y);
  }
}
