#!/bin/bash

SCREENSHOT_DIR="$HOME/Pictures/Screenshots"

mkdir -p "$SCREENSHOT_DIR"

TIMESTAMP=$(date +"%y-%m-%d_%H:%M:%S")

FILENAME="screenshot_${TIMESTAMP}.png"

maim -s "$SCREENSHOT_DIR/$FILENAME" && notify-send "Screenshot Captured" "Screentshot saved to $SCREENSHOT_DIR/$FILENAME"
