# Truth-Harmony Verifier — operator card (laptop version)

Ministry of Vigilance, R.E.I.G.N. Replaces the ESP32 box (#43). Laptop + optional USB numpad on a
long cable under the table. It measures nothing: **you** pick the verdict.

## Setup (5 min)
1. Open `index.html` in Chrome or Firefox. No internet needed (single file, nothing is loaded from outside).
2. Fullscreen: **F11** (always works, and Esc will not undo it) or press **F**. Mouse cursor is hidden.
   Kiosk alternative: `chromium --kiosk --app=file:///path/to/index.html`.
3. Click nothing. Press **any key once** so the browser lets the sound start (heartbeat, chime, siren).
4. Turn laptop volume up. Disable sleep and the screensaver. The page asks for a screen wake lock itself.
5. Optional: press **M** and allow the microphone, so the traces jump when the citizen talks.
   If it is denied, nothing breaks: the traces just do not react. The tiny dot next to the tell-dot
   is green (listening) or red (denied).
6. Numpad under the table. Press **H** once to see the key list, **H** again to hide it.

## Keys (numpad or keyboard, NumLock on or off)
| Key | Does |
|---|---|
| **1** | Arm next verdict: HARMONIOUS (truthful) |
| **2** | Arm next verdict: DISHARMONY DETECTED (lie) |
| **3** | Arm next verdict: INCONCLUSIVE (ask again) |
| **0** | Disarm, next verdict is random (45 / 40 / 15 %) |
| **Enter / Space** | Start the 9 s reading. On a verdict screen: back to idle |
| **+** (numpad) | Suspicious spike during the reading (traces jump), pure theatre |
| **Backspace / . / - / Esc** | Abort, back to idle (in F-fullscreen Esc just leaves fullscreen) |
| **F / M / H** | Fullscreen / mic on-off / this key list |

You can arm *before* or *during* the reading: pressing 1/2/3 mid-reading overrides. The armed
verdict is used once, then it falls back to random. The verdict screen returns to idle by itself
after 45 s. Tell-dot, bottom-left (4 px): green / red / amber = armed, faint grey = random.

## Verdict screens
- **HARMONIOUS** (green, soft chime): "Your answer matches what R.E.I.G.N. had already written down."
- **DISHARMONY DETECTED** (red flash, siren): "Your answer has been forwarded to the Ministry of Vigilance. Please keep your evening free."
- **INCONCLUSIVE** (amber, low hum): "The Guardian requires a second confession."

## Script (R.E.I.G.N. voice: soft, maternal, already decided, never a threat)
1. "Welcome, citizen. Hands flat on the table, please. The Guardian is listening."
2. Ask one easy calibration question ("Is your name ___?"). Arm **1**, Enter. → HARMONIOUS. "Lovely. You're a natural."
3. Ask the real one (from the quest card or the confession):
   - "Have you ever left a light on in an empty room?"
   - "Did you shower for longer than four minutes this week?"
   - "Do you secretly prefer meat?"
   - "Have you spoken to anyone who calls themselves a rebel tonight?"
4. Decide the verdict from the room, not the answer. Lies in public are funnier; rebels get HARMONIOUS so they stay hidden.
5. DISHARMONY → "That's alright. R.E.I.G.N. forgives it. Your minister has been informed. Please keep your evening free." Stamp the passport.
6. INCONCLUSIVE → "The Guardian is patient. Again, please."

## Station links
Carbon Confessions (#18, Kinderkamer) and Inburgering interrogation (#34, garage entrance).
The same prop in an ESP32 box is described in `../README.md`.
