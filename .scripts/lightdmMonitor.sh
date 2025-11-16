#!/bin/bash

if xrandr | grep -q "HDMI-A-0 connected"; then
	xrandr --output HDMI-A-0 --auto --output eDP --off
else
	xrandr --output eDP --auto --output HDMI-A-0 --off
fi
