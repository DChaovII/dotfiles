#!/bin/bash

case $1 in
    up)
        pamixer -i 2 --unmute
        ;;
    down)
        pamixer -d 2 --unmute
        ;;
    mute)
        pamixer -t
        ;;
esac

volume=$(pamixer --get-volume)
is_mute=$(pamixer --get-mute)

if [ "$is_mute" = "true" ] || [ "$volume" -eq 0 ]; then
    icon="audio-volume-muted-symbolic"
    msg="Muted"
    volume=0
else
    icon="audio-volume-high-symbolic"
    msg="${volume}%"
fi

# -h: progress bar
dunstify -a "changeVolume" -u low -i "$icon" -h int:value:"$volume" -h string:x-dunst-stack-tag:volume "$msg"

canberra-gtk-play -i audio-volume-change
