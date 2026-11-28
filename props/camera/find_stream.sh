#!/usr/bin/env bash
# Find a local RTSP stream on the LSC Smart Connect indoor camera (Tuya based).
# Many Tuya cams are cloud-only; this tells you in ~30 s whether a local stream exists.
# Usage: props/camera/find_stream.sh <camera-ip> [user] [password]
#   IP: LSC app -> camera -> settings -> device info, or your router's client list.
#   user/password: the ONVIF/stream password if the app lets you set one (NOT your LSC account password).
# On success it prints the working URL and opens it fullscreen with ffplay.
set -uo pipefail
IP="${1:?usage: $0 <camera-ip> [user] [password]}"; U="${2:-admin}"; P="${3:-}"
AUTH="$U${P:+:$P}@"

echo "== open ports on $IP"
for port in 554 8554 80 8080 6668 8000; do
  if timeout 1 bash -c "</dev/tcp/$IP/$port" 2>/dev/null; then echo "  $port open"; OPEN+=("$port"); fi
done
[[ " ${OPEN[*]:-} " == *" 554 "* || " ${OPEN[*]:-} " == *" 8554 "* ]] || {
  echo "No RTSP port (554/8554) open: this camera is cloud-only right now."
  echo "Check the LSC app for an ONVIF/RTSP switch; otherwise use the phone fallback in CAMERA_SETUP.md."
  exit 1; }

PATHS=(/ /live /h264_stream /onvif1 /onvif2 /stream1 /11 /12 /live/ch00_0 /ch0_0.h264 /Streaming/Channels/101 /cam/realmonitor?channel=1\&subtype=0)
for port in 554 8554; do
  for path in "${PATHS[@]}"; do
    for auth in "$AUTH" ""; do
      url="rtsp://${auth}${IP}:${port}${path}"
      if timeout 6 ffprobe -v error -rtsp_transport tcp -select_streams v:0 -show_entries stream=codec_name,width,height -of csv=p=0 "$url" >/tmp/cam_probe 2>/dev/null; then
        echo "FOUND: $url  ($(cat /tmp/cam_probe))"
        echo "$url" > "$(dirname "$0")/stream_url.txt"
        echo "Open: ffplay -fs -rtsp_transport tcp \"$url\"   (or VLC: Media > Open Network Stream)"
        exec ffplay -fs -loglevel error -rtsp_transport tcp "$url"
      fi
    done
  done
done
echo "RTSP port open but no path answered. Try your stream password: $0 $IP admin <password>"
exit 2
