#!/bin/sh
#dbus-update-activation-environment --all &

#killall snixembed 2>/dev/null
#(sleep 2 && snixembed) &

#kanshi &
/usr/bin/lxqt-policykit-agent &
dunst -conf "$HOME/.config/dunst/dunstrc" &
kime &
nm-applet --indicator &
$HOME/.screenlayout/ext_main.sh &
