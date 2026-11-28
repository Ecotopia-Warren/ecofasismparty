# Truth-Harmony Verifier (fake lie detector)

A standalone prop for the **Confession Pen** of the **Ministry of Vigilance** (R.E.I.G.N.,
Ecotopia). It measures nothing. A facilitator picks the verdict in secret, and the prop acts it
out. Verdicts, in this wording everywhere: **HARMONIOUS**, **DISHARMONY DETECTED**,
**INCONCLUSIVE**.

Two variants (issue #43):

| Variant | Where | Status |
|---|---|---|
| **Laptop app** (primary) | `laptop/index.html` + `laptop/OPERATOR.md` | One offline HTML file. Hidden numpad keys, heartbeat, chime, siren, optional mic. Start here |
| **ESP32 box** | `lie_detector/`, `dial_face.svg`, `make_dial.py` | Needle, LED bar, speaker. Remote by phone or hidden buttons. Compile-tested, see below |

## Laptop app (primary)

Open `laptop/index.html` in Chrome or Firefox (no network needed), press **F** (or F11) for
fullscreen. Operator keys and the script are in `laptop/OPERATOR.md`.

## ESP32 box

The firmware drives a servo needle, LED bar and speaker. The needle wanders nervously while
"measuring", then acts out the verdict you pick: a green glow and chime for **HARMONIOUS**, a
slam into the red with strobe and siren for **DISHARMONY DETECTED**.

## Parts (about €12)

| Part | Notes |
|---|---|
| ESP32 DevKit (WROOM-32) | Any common 30/38-pin board |
| SG90 or MG90S servo | Drives the needle. MG90S jitters less |
| WS2812 LED stick, 8 LEDs | Change `NUM_LEDS` if you use a different length |
| Small speaker (8 Ω, 0.5–1 W) + 100 Ω resistor | Wired across GPIO 26 and 27, with the resistor in series. A passive piezo also works |
| Red and green LEDs + 220 Ω resistors | Or two MOSFET/relay modules for real lamps |
| 3 momentary buttons (optional) | Hidden under the table on a long cable |
| 330 Ω resistor | In series with the LED data line |
| 5 V USB power bank (2 A) | Powers everything |

## Wiring

| ESP32 pin | Goes to |
|---|---|
| GPIO 18 | Servo signal (orange) |
| GPIO 5 → 330 Ω | WS2812 DIN |
| GPIO 26 → 100 Ω | Speaker lead 1 (tone) |
| GPIO 27 | Speaker lead 2 (firmware holds it LOW) |
| GPIO 25 → 220 Ω | Red LED (or MOSFET gate) |
| GPIO 23 → 220 Ω | Green LED (or MOSFET gate) |
| GPIO 13 / 32 / 33 | Hidden buttons SCAN / HARMONIOUS / DISHARMONY, other leg to GND |
| 5V (VIN) | Servo red + WS2812 5V |
| GND | Everything's GND (shared) |

Power the board from the power bank's USB port. The servo and LEDs take their 5 V from VIN.
If the needle twitches when the LEDs flash, put a 470–1000 µF capacitor across 5V/GND near the
servo.

## Flashing

```bash
arduino-cli core install esp32:esp32        # once (needs the Espressif board URL)
arduino-cli lib install "Adafruit NeoPixel" # once
arduino-cli compile --fqbn esp32:esp32:esp32 lie_detector
arduino-cli upload  --fqbn esp32:esp32:esp32 -p /dev/ttyUSB0 lie_detector
```

The Arduino IDE also works: open `lie_detector/lie_detector.ino` and pick the board
"ESP32 Dev Module".

## Operating it

**From a phone (main method):** join the Wi-Fi network **`HP-Print-4F-LaserJet`** (password
`harmony2026`) and open **http://192.168.4.1**. The network looks like a printer and the page is
titled "Print queue", so a glance at your screen gives nothing away. Android may warn about
"no internet"; choose *stay connected*.

| Button | Effect |
|---|---|
| **SCAN** | Starts measuring: the needle wanders nervously and ticks. Press it as the citizen starts answering |
| **SUSPICIOUS SPIKE** | The needle jumps into the red and settles again. Use it for theatre in the middle of an answer |
| **HARMONIOUS** | About 2.5 s of rising drama, then the needle drops to HARMONIOUS with a green glow and a chime. Back to idle after 8 s |
| **DISHARMONY** | About 2.5 s of rising drama, then the needle slams into DISHARMONY with a red strobe and siren. Back to idle after 12 s |
| **RESET** | Back to idle immediately |
| **MUTE** | Turns sound on or off, for the quiet hours |

**Hidden buttons:** SCAN, HARMONIOUS and DISHARMONY do the same as above.

**USB serial (bench test, 115200 baud):** `s` scan, `k` spike, `t` truth, `l` lie, `r` reset,
`m` mute.

## Dial face

`dial_face.svg` (180 × 120 mm) has a 144° scale that matches the default servo sweep. Print it
at 100% and glue it to card, or engrave it on 4 mm poplar at Bitlair. The ring marks where the
servo shaft goes. To change it, edit `make_dial.py` and run `python3 make_dial.py`.

For the needle, use a thin strip of red acrylic or a painted bamboo skewer pushed onto a servo
horn. To calibrate, send `r` and adjust `SERVO_US_LEFT` until the needle sits at 0. Then send `l`
(DISHARMONY) and adjust `SERVO_US_RIGHT` until it sits at 100.

## Suggested Confession Pen script

Voice: soft, maternal, already decided. R.E.I.G.N. never threatens.

1. Seat the citizen and put two "electrodes" on their fingers: copper tape on a strap, connected
   to nothing. "Welcome, citizen. The Guardian is listening."
2. Ask a calibration question ("Is your name ___?"). Press **HARMONIOUS**. "Lovely. You're a natural."
3. Ask the real question ("Did you fly last year?"). Press **SCAN** while they answer,
   **SPIKE** at a suspicious pause, then **DISHARMONY**.
4. "That's alright. Your answer has been forwarded to the Ministry of Vigilance. Please keep
   your evening free."
