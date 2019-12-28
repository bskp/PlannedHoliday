#define DT  1100

void setup() {
  pinMode(14, INPUT);
  attachInterrupt(14, handleIr, FALLING);

  pinMode(LED_BUILTIN, OUTPUT);
}

volatile boolean fb_on = false;

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED_BUILTIN, LOW);
}

void handleCode(short code) {
  Serial.println(code);
  
}

void handleIr() {
  static long last = 0;
  long now = micros();
  int l = (now - last - DT/2)/DT;

  static unsigned short code = 0x0000;
  static short idx = 0;
  if (l < 2) {
    if (idx >= 16) {
      code |= l << 30 - idx;
    }
    idx++;

    if (idx == 32) {
      handleCode(code);
    }
  } 
  else {
    idx = 0;
    code = 0x0000;
  }

  last = now;
  digitalWrite(LED_BUILTIN, HIGH);
}
