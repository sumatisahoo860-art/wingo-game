#!/usr/bin/env bash
# एरर आने पर स्क्रिप्ट रोकें
set -o errexit

# पाइथन डिपेंडेंसी इंस्टॉल करें
pip install -r requirements.txt

# सर्वर पर क्रोम ब्राउज़र डाउनलोड और इंस्टॉल करें
STORAGE_DIR=/opt/render/project/.render
mkdir -p $STORAGE_DIR

if [ ! -d "$STORAGE_DIR/chrome" ]; then
  echo "Chrome इंस्टॉल किया जा रहा है..."
  wget -q https://googleapis.com
  unzip -q chrome-linux64.zip
  mv chrome-linux64 $STORAGE_DIR/chrome
  rm chrome-linux64.zip
  
  wget -q https://googleapis.com
  unzip -q chromedriver-linux64.zip
  mv chromedriver-linux64 $STORAGE_DIR/chromedriver
  rm chromedriver-linux64.zip
fi
