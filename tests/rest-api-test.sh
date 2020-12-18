#!/bin/bash

echo "[-] Running Endpoints tests on dycow."
success_tests=0
failed_tests=0

content=$(curl -s http://127.0.0.1:1237/)
if [[ "$content" == *"Hello world"* ]]
then
  success_tests=$((success_tests+1))
  echo "[✓] GET / passed."
else
  failed_tests=$((failed_tests+1))
  echo "[X] GET / failed."
fi

content=$(curl -s http://127.0.0.1:1237/list)
if [[ "$content" == *"total"* ]]
then
  success_tests=$((success_tests+1))
  echo "[✓] GET /list passed."
else
  failed_tests=$((failed_tests+1))
  echo "[X] GET /list failed."
fi

content=$(curl -s http://127.0.0.1:1237/callme?name=darker)
if [[ "$content" == *"Thanks darker !"* ]]
then
  success_tests=$((success_tests+1))
  echo "[✓] GET /callme?name=darker passed."
else
  failed_tests=$((failed_tests+1))
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
  success_tests=$((success_tests+1))
  echo "[✓] POST /save passed."
else
  failed_tests=$((failed_tests+1))
  echo "[X] POST /save failed."
fi

echo "- - -"
echo "[-] Tests run :"
echo "[-] $success_tests tests succeed !"
echo "[-] $failed_tests tests failed !"

echo "[-] Stopping tests Endpoints on dycow."

