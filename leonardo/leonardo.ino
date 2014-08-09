// In arduino-1.0.x/hardware/arduino/cores/arduino/CDC.cpp
// change SERIAL_BUFFER_SIZE to 2048 to prevent buffer overflow
// on large CDC incoming packets (since 1pkt/ms we have time to
// write them to the bus eventually but need more buffer to 
// hold them beforehand. note that 2.5k ram on this chip so
// 2k is a lot of it, but this code only uses 155 bytes so we're
// OK really)

const int datapin = 10;
const int srckpin = 11;
const int rckpin = 12;

void setup()
{
  Serial.begin(115200);
  
  pinMode(datapin, OUTPUT);
  pinMode(srckpin, OUTPUT);
  pinMode(rckpin, OUTPUT);

  digitalWrite(srckpin, LOW);
  digitalWrite(rckpin, LOW);
}

void wait()
{
  delayMicroseconds(1);
}

// Clocks out the LSB of thebit using srck
void txbit(int thebit)
{
    digitalWrite(datapin, thebit & 1);
    wait();
    digitalWrite(srckpin, HIGH);
    wait();
    digitalWrite(srckpin, LOW);
    wait();
}

// Clocks out thebyte, LSB first.
void txbyte(int thebyte)
{
    txbit(0); // First bit is ignored
    for(int i=0; i<7; i++)
      txbit(thebyte >> i);
}

void loop()
{
  int rows[7];

  while(!Serial.available() || Serial.read() != 0x02); // Wait for start byte
  while(Serial.available() < 8); // Wait for a packet
  for(int i=0; i<7; i++)
      rows[i] = Serial.read();
  if(Serial.read() == 0x03)
  {
    for(int i=0; i<7; i++)
      txbyte(rows[i]);
    digitalWrite(rckpin, HIGH);
    wait();
    digitalWrite(rckpin, LOW);
    wait();
  }
}
