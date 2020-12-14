#!/bin/bash

echo "[-] Running Endpoints tests on dycow."

content=$(curl -s http://127.0.0.1:1237/)
if [[ "$content" == *"Hello world"* ]]
then
  echo "[✓] GET / passed."
else
  echo "[X] GET / failed."
fi

content=$(curl -s http://127.0.0.1:1237/list)
if [[ "$content" == *"total"* ]]
then
  echo "[✓] GET /list passed."
else
  echo "[X] GET /list failed."
fi

content=$(curl -s http://127.0.0.1:1237/callme?name=darker)
if [[ "$content" == *"Thanks darker !"* ]]
then
  echo "[✓] GET /callme?name=darker passed."
else
  echo "[X] GET /callme?name=darker failed."
fi

content=$(curl --location --request POST -s 'http://127.0.0.1:1237/save' \
--header ': ' \
--data-raw '{
    "name": "test",
    "content": "Big text"
}')
if [[ "$content" == *"request sent."* ]]
then
  echo "[✓] POST /save passed."
else
  echo "[X] POST /save failed."
fi

echo "[-] Stopping tests Endpoints on dycow."

