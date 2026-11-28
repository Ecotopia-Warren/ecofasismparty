// Talk test: SAM robot voice, speaker across GPIO 26 / 27 (no amp).
// Each sentence is rendered to RAM first, then played at an exact 22050 Hz
// as high-frequency PWM on GPIO 26 (drives a bare speaker much harder than the DAC).
// Serial (115200): type text + Enter to speak.  "v 1.5" sets volume, "p 70" vPitch, "s 72" vSpeed.
#include <ESP8266SAM.h>
#include <AudioOutput.h>

const int PIN_SPK = 26;
const int PIN_SPK_B = 27;        // driven with the inverted signal (bridge drive, ~4x power)
const int RATE = 22050;
size_t MAX_SAMPLES = 0;  // set from free heap at boot

float volume = 1.0f;
int vPitch = 85, vSpeed = 90;   // SAM: higher pitch value = deeper voice, higher speed value = slower

uint8_t *buf = nullptr;
size_t len = 0;

class BufOut : public AudioOutput {
 public:
  bool SetRate(int) override { return true; }
  bool begin() override { len = 0; return true; }
  bool ConsumeSample(int16_t s[2]) override {
    if (buf && len < MAX_SAMPLES) buf[len++] = (uint8_t)((s[0] >> 8) + 128);
    return true;
  }
  bool stop() override { return true; }
};

BufOut out;
ESP8266SAM sam;

void spk(int duty) {               // same duty on both pins; pin B is inverted in hardware
  ledcWrite(PIN_SPK, duty);
  ledcWrite(PIN_SPK_B, duty);
}

void play() {
  // normalise: scale the loudest peak to full range
  int peak = 1;
  for (size_t i = 0; i < len; i++) peak = max(peak, abs((int)buf[i] - 128));
  float gain = volume * 127.0f / peak;
  const uint32_t periodNs = 1000000000UL / RATE;  // 45351 ns
  uint64_t t0 = esp_timer_get_time() * 1000ULL;
  for (size_t i = 0; i < len; i++) {
    int v = 128 + (int)((buf[i] - 128) * gain);
    spk(constrain(v, 0, 256));
    uint64_t due = t0 + (uint64_t)(i + 1) * periodNs;
    while (esp_timer_get_time() * 1000ULL < due) {}
  }
  spk(128);
  delay(20);
  spk(0);   // both pins LOW: silence, no current through the speaker
}

void say(const char *s) {
  sam.SetPitch(vPitch);
  sam.SetSpeed(vSpeed);
  sam.Say(&out, s);
  Serial.printf("SAY (%u samples, %.1fs): %s\n", (unsigned)len, len / (float)RATE, s);
  play();
}

void setup() {
  Serial.begin(115200);
  // channels 0 and 1 share LEDC timer 0, so both pins switch in phase
  ledcAttachChannel(PIN_SPK, 312500, 8, 0);    // 80 MHz / 256 = 312.5 kHz carrier, inaudible
  ledcAttachChannel(PIN_SPK_B, 312500, 8, 1);
  ledcOutputInvert(PIN_SPK_B, true);
  spk(0);
  size_t largest = heap_caps_get_largest_free_block(MALLOC_CAP_8BIT);
  MAX_SAMPLES = largest > 40000 ? largest - 30000 : 0;   // leave room for SAM's own buffers
  buf = (uint8_t *)malloc(MAX_SAMPLES);
  if (!buf) { MAX_SAMPLES = 0; Serial.println("no memory for audio buffer"); }
  Serial.printf("audio buffer: %u samples (%.1f s max per sentence)\n", (unsigned)MAX_SAMPLES, MAX_SAMPLES / (float)RATE);
  sam.SetVoice(ESP8266SAM::VOICE_SAM);
  delay(300);
  say("Attention citizen. The Guardian is listening.");
  delay(300);
  say("This is a truth harmony inspection. Questions are welcome. They have already been answered.");
  Serial.println("Type text + Enter. Commands: v <volume>, p <pitch>, s <speed>");
}

void loop() {
  if (!Serial.available()) return;
  String s = Serial.readStringUntil('\n');
  s.trim();
  if (s.startsWith("v ")) { volume = s.substring(2).toFloat(); Serial.printf("volume %.2f\n", volume); }
  else if (s.startsWith("p ")) { vPitch = s.substring(2).toInt(); Serial.printf("pitch %d\n", vPitch); }
  else if (s.startsWith("s ")) { vSpeed = s.substring(2).toInt(); Serial.printf("speed %d\n", vSpeed); }
  else if (s.length()) say(s.c_str());
}
