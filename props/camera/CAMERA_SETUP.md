# Camera: LSC Smart Connect Indoor IP Camera (Action, art. 3215672.3)

Tuya-based, **2.4 GHz Wi-Fi only** (WPA/WPA2), set up with the **LSC Smart Connect** app. Range ~50 m.

## Goal for tonight (Epic #73)
"R.E.I.G.N. is watching": a live feed on a laptop/TV screen as decoration. **Show live only, record nothing.**

## Setup (15 min)
1. Phone on the venue **2.4 GHz** network (not 5 GHz, not a guest network with client isolation). Install **LSC Smart Connect**, add the camera, scan its QR code.
2. In the app: **turn off** cloud storage / SD recording, motion alerts and sound detection. Set the time zone.
3. Look for an **ONVIF / RTSP** switch in the camera settings. If it exists, switch it on and set a stream password.
4. On the screen laptop (same network): `props/camera/find_stream.sh <camera-ip> admin <stream-password>`
   - **FOUND** → it opens the feed fullscreen. For a permanent party screen run `kiosk_setup.sh` from the laptop rescue kit, or just leave ffplay/VLC fullscreen.
   - **cloud-only** → use the fallback.

## Fallback (always works)
Old phone/tablet with the LSC app, live view fullscreen, plugged into power, screen timeout off. Bigger: mirror the phone to a TV or laptop (Chromecast / Miracast / `scrcpy` over USB on Linux).

## Consent and privacy (#76)
- Sign at the camera and at customs: *"R.E.I.G.N. is watching. Live feed only: nothing is recorded or stored."*
- **Not** in toilets, the consent station, changing/sleeping rooms or the Kinderkamer.
- Tuya cameras stream via the manufacturer's cloud. Unplug the camera after the party and remove it from the app.

## Test on site (#77)
- [ ] Wi-Fi signal at the mount spot (app shows live view without stutter)
- [ ] Feed on the screen for 10 minutes without freezing
- [ ] Recording off, sign up
- [ ] Power cable taped down, out of reach
