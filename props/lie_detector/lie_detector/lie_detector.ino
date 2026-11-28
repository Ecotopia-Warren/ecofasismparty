// ============================================================================
//  TRUTH-HARMONY VERIFIER  (a completely fake lie detector)
//  Ministry of Vigilance, R.E.I.G.N. Ecotopia. Verdicts: HARMONIOUS / DISHARMONY DETECTED.
//  Standalone prop for the Confession Pen (Ministry of Vigilance). ESP32 DevKit (WROOM-32).
//
//  The verdict is decided by a facilitator, never by the "subject":
//    - from a phone: join the hidden Wi-Fi, open http://192.168.4.1
//    - or with hidden buttons under the table (optional)
//    - or over USB serial for bench tests (s/k/t/l/r/m)
//
//  Outputs: servo needle on a printed dial, WS2812 LED bar, speaker (26/27),
//           red + green lamps (LEDs, or MOSFET/relay for bigger lights).
//
//  Dial convention: LEFT = calm / HARMONIOUS (green), RIGHT = DISHARMONY (red).
//  Needs the "Adafruit NeoPixel" library. Works on ESP32 Arduino core 2.x and 3.x.
// ============================================================================

#include <WiFi.h>
#include <WebServer.h>
#include <Adafruit_NeoPixel.h>

// ---------------------------- configuration ---------------------------------
// The Wi-Fi name is deliberately boring so guests don't spot the remote.
const char *AP_SSID = "HP-Print-4F-LaserJet";
const char *AP_PASS = "harmony2026";   // min 8 chars

const int PIN_SERVO   = 18;  // needle servo signal (SG90 / MG90S)
const int PIN_LEDS    = 5;   // WS2812 data in (via ~330 ohm)
const int PIN_BUZZER  = 26;  // speaker lead 1 (tone output)
const int PIN_SPK_GND = 27;  // speaker lead 2 (held LOW as speaker ground)
const int PIN_LAMP_R  = 25;  // red lamp / LED  (HIGH = on)
const int PIN_LAMP_G  = 23;  // green lamp / LED (HIGH = on)
const int PIN_BTN_SCAN  = 13; // hidden buttons: to GND, internal pull-up
const int PIN_BTN_TRUTH = 32;
const int PIN_BTN_LIE   = 33;

const int NUM_LEDS       = 8;    // LED stick length
const int LED_BRIGHTNESS = 90;   // 0-255, keep modest on USB power

// Servo travel. Adjust so the needle covers your printed dial exactly.
const int SERVO_US_LEFT  = 2300; // pulse at level 0 (HARMONIOUS end)
const int SERVO_US_RIGHT = 700;  // pulse at level 1000 (DISHARMONY end)

const uint32_t BUILDUP_MS    = 2600;  // drama before a verdict
const uint32_t LIE_HOLD_MS   = 12000; // then back to idle
const uint32_t TRUTH_HOLD_MS = 8000;
const uint32_t SCAN_TIMEOUT  = 90000; // forgotten scan returns to idle

// LEDC channels: servo and buzzer must sit on different timers
// (timer = channel / 2), otherwise every beep would twitch the needle.
const int CH_SERVO  = 0;
const int CH_BUZZER = 2;

// ------------------------------ state ---------------------------------------
enum Mode { IDLE, SCANNING, BUILDUP, LIE, TRUTH };
const char *MODE_NAMES[] = {"IDLE", "SCANNING", "ANALYSING", "DISHARMONY", "HARMONIOUS"};

Mode mode = IDLE;
Mode pendingVerdict = LIE;
uint32_t modeStart = 0;
bool muted = false;

// Needle physics: a spring-damper so it overshoots and wobbles like a real meter.
float needlePos = 0, needleVel = 0, needleTarget = 60;
float springK = 0.020f, damping = 0.86f;
uint32_t nextWander = 0;
uint32_t spikeUntil = 0;

enum Sound { SND_NONE, SND_TICK, SND_CHIRP, SND_SIREN, SND_CHIME, SND_BOOT };
Sound sound = SND_NONE;
uint32_t soundStart = 0;
uint32_t nextTick = 0;
int lastFreq = -1;

Adafruit_NeoPixel strip(NUM_LEDS, PIN_LEDS, NEO_GRB + NEO_KHZ800);
WebServer server(80);

// ------------------------- LEDC compatibility -------------------------------
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  #define SERVO_ATTACH()      ledcAttachChannel(PIN_SERVO, 50, 16, CH_SERVO)
  #define SERVO_WRITE(d)      ledcWrite(PIN_SERVO, d)
  #define BUZZER_ATTACH()     ledcAttachChannel(PIN_BUZZER, 2000, 10, CH_BUZZER)
  #define BUZZER_TONE(f)      ledcWriteTone(PIN_BUZZER, f)
#else
  #define SERVO_ATTACH()      do { ledcSetup(CH_SERVO, 50, 16); ledcAttachPin(PIN_SERVO, CH_SERVO); } while (0)
  #define SERVO_WRITE(d)      ledcWrite(CH_SERVO, d)
  #define BUZZER_ATTACH()     do { ledcSetup(CH_BUZZER, 2000, 10); ledcAttachPin(PIN_BUZZER, CH_BUZZER); } while (0)
  #define BUZZER_TONE(f)      ledcWriteTone(CH_BUZZER, f)
#endif

// ------------------------------ helpers -------------------------------------
void setMode(Mode m) {
  mode = m;
  modeStart = millis();
  Serial.printf("[mode] %s\n", MODE_NAMES[m]);
}

void playSound(Sound s) {
  sound = s;
  soundStart = millis();
}

void setTone(int f) {
  if (muted) f = 0;
  if (f == lastFreq) return;
  lastFreq = f;
  BUZZER_TONE(f);
}

// --------------------------- commands ---------------------------------------
void cmdScan() {
  setMode(SCANNING);
  springK = 0.020f; damping = 0.86f;
  needleTarget = 250;
  playSound(SND_CHIRP);
}

void cmdSpike() {  // a "suspicious reading" mid-answer, no verdict
  if (mode != SCANNING) cmdScan();
  spikeUntil = millis() + 900;
  needleTarget = random(720, 880);
  playSound(SND_CHIRP);
}

void cmdVerdict(Mode v) {
  pendingVerdict = v;
  springK = 0.030f; damping = 0.84f;
  setMode(BUILDUP);
}

void cmdReset() {
  setMode(IDLE);
  springK = 0.015f; damping = 0.88f;
  playSound(SND_NONE);
}

void handleCommand(const String &c) {
  if      (c == "scan")  cmdScan();
  else if (c == "spike") cmdSpike();
  else if (c == "truth") cmdVerdict(TRUTH);
  else if (c == "lie")   cmdVerdict(LIE);
  else if (c == "reset") cmdReset();
  else if (c == "mute")  { muted = !muted; setTone(0); }
}

// --------------------------- needle -----------------------------------------
void updateTargets(uint32_t now) {
  uint32_t t = now - modeStart;
  switch (mode) {
    case IDLE:
      // slow breathing near the calm end
      needleTarget = 60 + 25 * sinf(now / 1400.0f);
      break;

    case SCANNING:
      if (now < spikeUntil) break;
      if (now >= nextWander) {
        // nervous random walk in the middle of the scale
        needleTarget = constrain(needleTarget + random(-160, 170), 150, 620);
        nextWander = now + random(110, 380);
      }
      if (now >= nextTick) { playSound(SND_TICK); nextTick = now + random(350, 650); }
      if (t > SCAN_TIMEOUT) cmdReset();
      break;

    case BUILDUP: {
      // growing oscillation with accelerating ticks
      float p = (float)t / BUILDUP_MS;                 // 0..1
      float amp = 120 + 330 * p;
      needleTarget = 480 + amp * sinf(t / (160.0f - 90.0f * p));
      uint32_t gap = 320 - (uint32_t)(260 * p);
      if (now >= nextTick) { playSound(SND_TICK); nextTick = now + gap; }
      if (t >= BUILDUP_MS) {
        if (pendingVerdict == LIE) {
          springK = 0.06f; damping = 0.80f;            // slam
          needleTarget = 975;
          playSound(SND_SIREN);
        } else {
          springK = 0.025f; damping = 0.85f;
          needleTarget = 70;
          playSound(SND_CHIME);
        }
        setMode(pendingVerdict);
      }
      break;
    }

    case LIE:
      // pinned against the stop, trembling
      needleTarget = 965 + 25 * sinf(now / 45.0f);
      if (t > LIE_HOLD_MS) cmdReset();
      break;

    case TRUTH:
      needleTarget = 70 + 10 * sinf(now / 900.0f);
      if (t > TRUTH_HOLD_MS) cmdReset();
      break;
  }
}

void stepNeedle() {
  needleVel += (needleTarget - needlePos) * springK;
  needleVel *= damping;
  needlePos += needleVel;
  float lvl = constrain(needlePos, 0.0f, 1000.0f);
  int us = SERVO_US_LEFT + (int)((SERVO_US_RIGHT - SERVO_US_LEFT) * lvl / 1000.0f);
  SERVO_WRITE((uint32_t)us * 65535UL / 20000UL);
}

// ---------------------------- sound -----------------------------------------
void updateSound(uint32_t now) {
  uint32_t t = now - soundStart;
  int f = 0;
  switch (sound) {
    case SND_NONE: f = 0; break;
    case SND_TICK:
      f = (t < 9) ? 1900 : 0;
      if (t >= 9) sound = SND_NONE;
      break;
    case SND_CHIRP:
      if (t < 140) f = 2600 - t * 7; else sound = SND_NONE;
      break;
    case SND_SIREN:   // wailing alarm for ~3.5 s
      if (t < 3500) f = 750 + (int)(550 * (0.5f + 0.5f * sinf(t * 2 * PI / 650.0f)));
      else sound = SND_NONE;
      break;
    case SND_CHIME:   // two-tone "harmony confirmed"
      if      (t < 170) f = 988;
      else if (t < 210) f = 0;
      else if (t < 650) f = 1319;
      else sound = SND_NONE;
      break;
    case SND_BOOT:
      if      (t < 120) f = 660;
      else if (t < 240) f = 880;
      else if (t < 380) f = 1320;
      else sound = SND_NONE;
      break;
  }
  setTone(f);
}

// ----------------------------- lights ---------------------------------------
uint32_t barColor(int i) {  // green -> yellow -> red along the bar
  float x = (float)i / (NUM_LEDS - 1);
  uint8_t r = x < 0.5f ? (uint8_t)(510 * x) : 255;
  uint8_t g = x < 0.5f ? 255 : (uint8_t)(510 * (1 - x));
  return strip.Color(r, g, 0);
}

void updateLights(uint32_t now) {
  uint32_t t = now - modeStart;
  bool lampR = false, lampG = false;
  strip.clear();

  if (mode == IDLE) {
    uint8_t b = 20 + (uint8_t)(20 * (0.5f + 0.5f * sinf(now / 900.0f)));
    strip.setPixelColor(0, strip.Color(0, b / 2, b));
  } else if (mode == SCANNING || mode == BUILDUP) {
    float lvl = constrain(needlePos, 0.0f, 1000.0f) / 1000.0f;
    int lit = (int)(lvl * NUM_LEDS + 0.5f);
    for (int i = 0; i < NUM_LEDS && i < max(lit, 1); i++) strip.setPixelColor(i, barColor(i));
    if (mode == BUILDUP) lampR = (now / 120) % 2;   // nervous flicker
  } else if (mode == LIE) {
    bool on = (now / 140) % 2;
    for (int i = 0; i < NUM_LEDS; i++) strip.setPixelColor(i, on ? strip.Color(255, 0, 0) : 0);
    lampR = (t < 4000) ? on : true;                 // strobe, then steady
  } else if (mode == TRUTH) {
    uint8_t g = 120 + (uint8_t)(100 * (0.5f + 0.5f * sinf(now / 300.0f)));
    for (int i = 0; i < NUM_LEDS; i++) strip.setPixelColor(i, strip.Color(0, g, 20));
    lampG = true;
  }
  strip.show();
  digitalWrite(PIN_LAMP_R, lampR);
  digitalWrite(PIN_LAMP_G, lampG);
}

// ---------------------------- buttons ---------------------------------------
struct Btn { int pin; const char *cmd; bool last; uint32_t changed; };
Btn buttons[] = {
  {PIN_BTN_SCAN,  "scan",  true, 0},
  {PIN_BTN_TRUTH, "truth", true, 0},
  {PIN_BTN_LIE,   "lie",   true, 0},
};

void updateButtons(uint32_t now) {
  for (auto &b : buttons) {
    bool v = digitalRead(b.pin);
    if (v != b.last && now - b.changed > 40) {
      b.changed = now;
      b.last = v;
      if (!v) handleCommand(b.cmd);   // pressed (active low)
    }
  }
}

// ------------------------------ serial --------------------------------------
void updateSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    switch (c) {
      case 's': handleCommand("scan");  break;
      case 'k': handleCommand("spike"); break;
      case 't': handleCommand("truth"); break;
      case 'l': handleCommand("lie");   break;
      case 'r': handleCommand("reset"); break;
      case 'm': handleCommand("mute");  break;
    }
  }
}

// ------------------------------ web UI --------------------------------------
const char PAGE[] PROGMEM = R"HTML(<!doctype html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>Print queue</title><style>
body{margin:0;font-family:system-ui,sans-serif;background:#111;color:#ddd;padding:12px}
#st{text-align:center;font-size:14px;opacity:.7;margin:4px 0 12px}
.g{display:grid;grid-template-columns:1fr 1fr;gap:10px}
button{font-size:19px;font-weight:700;padding:26px 0;border:0;border-radius:14px;color:#fff}
.scan{background:#345}.spike{background:#864}.truth{background:#1a6b3a}.lie{background:#a11}
.reset{background:#333}.mute{background:#222;font-size:16px}
.w{grid-column:1/3}
</style></head><body>
<div id="st">...</div>
<div class="g">
<button class="scan w" onclick="c('scan')">SCAN</button>
<button class="spike w" onclick="c('spike')">SUSPICIOUS SPIKE</button>
<button class="truth" onclick="c('truth')">HARMONIOUS</button>
<button class="lie" onclick="c('lie')">DISHARMONY</button>
<button class="reset" onclick="c('reset')">RESET</button>
<button class="mute" onclick="c('mute')">MUTE</button>
</div>
<script>
function c(x){navigator.vibrate&&navigator.vibrate(30);fetch('/cmd?c='+x).then(r=>r.text()).then(t=>st.textContent=t)}
setInterval(()=>fetch('/state').then(r=>r.text()).then(t=>st.textContent=t).catch(()=>st.textContent='offline'),1500)
</script></body></html>)HTML";

String stateText() {
  return String(MODE_NAMES[mode]) + (muted ? " (muted)" : "");
}

void setupWeb() {
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASS);
  server.on("/", []() { server.send_P(200, "text/html", PAGE); });
  server.on("/cmd", []() {
    handleCommand(server.arg("c"));
    server.send(200, "text/plain", stateText());
  });
  server.on("/state", []() { server.send(200, "text/plain", stateText()); });
  server.onNotFound([]() { server.sendHeader("Location", "/"); server.send(302); });
  server.begin();
  Serial.printf("Remote: join Wi-Fi \"%s\" (pw %s), open http://%s\n",
                AP_SSID, AP_PASS, WiFi.softAPIP().toString().c_str());
}

// ------------------------------ main ----------------------------------------
void setup() {
  Serial.begin(115200);
  randomSeed(esp_random());

  pinMode(PIN_LAMP_R, OUTPUT);
  pinMode(PIN_LAMP_G, OUTPUT);
  pinMode(PIN_SPK_GND, OUTPUT);
  digitalWrite(PIN_SPK_GND, LOW);
  for (auto &b : buttons) pinMode(b.pin, INPUT_PULLUP);

  SERVO_ATTACH();
  BUZZER_ATTACH();
  setTone(0);

  strip.begin();
  strip.setBrightness(LED_BRIGHTNESS);
  strip.show();

  setupWeb();
  Serial.println("Serial keys: s=scan k=spike t=truth l=lie r=reset m=mute");

  setMode(IDLE);
  playSound(SND_BOOT);
}

void loop() {
  static uint32_t lastStep = 0;
  uint32_t now = millis();

  server.handleClient();
  updateButtons(now);
  updateSerial();

  if (now - lastStep >= 10) {        // 100 Hz animation tick
    lastStep = now;
    updateTargets(now);
    stepNeedle();
    updateSound(now);
    updateLights(now);
  }
}
