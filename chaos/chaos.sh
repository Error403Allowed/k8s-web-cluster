#!/bin/sh
while true; do
  TARGET=$(shuf -e web1 web2 web3 -n 1)
  echo "[chaos] Killing $TARGET"
  docker kill "$TARGET" 2>/dev/null && echo "[chaos] $TARGET killed"
  SLEEP=$(( (RANDOM % 30) + 15 ))
  sleep "$SLEEP"
done
