#include <RMCS2303drive.h>

RMCS2303 rmcs;

byte slave_id_1 = 7;
byte slave_id_2 = 6;

int INP_CONTROL_MODE = 257;
int PP_gain = 32;
int PI_gain = 16;
int VF_gain = 32;
int LPR = 334;
int acceleration = 5000;
int speed = 8000;

long int Current_Speed;

const byte START_BYTE = 0xAA;
const byte END_BYTE = 0xBB;
const int MAX_MESSAGE_SIZE = 6;

byte receivedMessage[MAX_MESSAGE_SIZE];
int messageIndex = 0;
bool readingMessage = false;

void setSpeed(byte slaveID, unsigned int speed)
{
  rmcs.Speed(slaveID, speed);
}

void getSpeed(byte slaveID)
{
  Current_Speed = rmcs.Speed_Feedback(slaveID);
  Serial.print("getSpeed : ");
  Serial.print(slaveID, DEC);
  Serial.print(" ");
  Serial.println(Current_Speed);
}

void motorEnableForward(byte slaveID)
{
  rmcs.Enable_Digital_Mode(slaveID, 0);
}

void motorEnableBackward(byte slaveID)
{
  rmcs.Enable_Digital_Mode(slaveID, 1);
}

void motorBrakeForward(byte slaveID)
{
  rmcs.Brake_Motor(slaveID, 0);
}

void motorBrakeBackward(byte slaveID)
{
  rmcs.Brake_Motor(slaveID, 1);
}

void motorDisable(byte slaveID)
{
  rmcs.Disable_Digital_Mode(slaveID, 1);
}

void executeCommand()
{
  byte command = receivedMessage[1];
  byte slaveID = receivedMessage[2];
  unsigned int speed = 0;

  if (command == 0x01 && messageIndex == 6)
  {
    speed = (receivedMessage[3] << 8) | receivedMessage[4];
    setSpeed(slaveID, speed);
  }
  else if (command == 0x02)
  {
    getSpeed(slaveID);
  }
  else if (command == 0x03)
  {
    motorEnableForward(slaveID);
  }
  else if (command == 0x04)
  {
    motorEnableBackward(slaveID);
  }
  else if (command == 0x05)
  {
    motorBrakeForward(slaveID);
  }
  else if (command == 0x06)
  {
    motorBrakeBackward(slaveID);
  }
  else if (command == 0x07)
  {
    motorDisable(slaveID);
  }
}

void setup()
{

  Serial.println("Opening Serial port...");
  rmcs.Serial_selection(0);
  rmcs.Serial0(115200);

  rmcs.begin(&Serial1, 9600);

  Serial.println("Writing parameters to board 1...");
  rmcs.WRITE_PARAMETER(slave_id_1, INP_CONTROL_MODE, PP_gain, PI_gain, VF_gain, LPR, acceleration, speed);

  Serial.println("Writing parameters to board 2...");
  rmcs.WRITE_PARAMETER(slave_id_2, INP_CONTROL_MODE, PP_gain, PI_gain, VF_gain, LPR, acceleration, speed);

  Serial.println("Reading parameters from board 1...");
  rmcs.READ_PARAMETER(slave_id_1);

  Serial.println("Reading parameters from board 2...");
  rmcs.READ_PARAMETER(slave_id_2);

  rmcs.Disable_Digital_Mode(slave_id_1, 1);
  rmcs.Disable_Digital_Mode(slave_id_2, 1);

  Serial.println("ARDUINO_READY");
}

void loop()
{

  if (Serial.available())
  {
    byte incomingByte = Serial.read();

    if (incomingByte == START_BYTE && !readingMessage)
    {
      readingMessage = true;
      messageIndex = 0;
      receivedMessage[messageIndex++] = incomingByte;
    }
    else if (readingMessage)
    {
      receivedMessage[messageIndex++] = incomingByte;

      if (incomingByte == END_BYTE || messageIndex >= MAX_MESSAGE_SIZE)
      {
        readingMessage = false;

        // Serial.print("Received bytes: [ ");
        // for (int i = 0; i < messageIndex; i++) {
        //   Serial.print("0x");
        //   Serial.print(receivedMessage[i], HEX);
        //   if (i < messageIndex - 1) {
        //     Serial.print(", ");
        //   }
        // }
        // Serial.println(" ]");

        executeCommand();

        messageIndex = 0;
      }
    }
  }
}
