void setup() {
  pinMode(1, OUTPUT);
  Serial1.begin(115200);
}

void loop() {
  Serial1.write(0xCA);
  Serial1.write(0xFE);
  Serial1.write(0xBA);
  Serial1.write(0xBE);
  Serial1.write((uint8_t)0x00);
}
