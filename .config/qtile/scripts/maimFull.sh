#!/bin/bash

SCREENSHOT_DIR="$HOME/Pictures/Screenshots"

mkdir -p "$SCREENSHOT_DIR"

TIMESTAMP=$(date +"%y-%m-%d_%H:%M:%S")

FILENAME="screenshot_${TIMESTAMP}.png"

maim "$SCREENSHOT_DIR/$FILENAME" && notify-send "Screenshot" "Screentshot save to $SCREENSHOT_DIR/$FILENAME"
