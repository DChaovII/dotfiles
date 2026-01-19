export GTK_IM_MODULE=kime
export QT_IM_MODULE=kime
export XMODIFIERS=@im=kime
export QT_QPA_PLATFORMTHEME=qt5ct

/usr/bin/lxqt-policykit-agent &
dunst -conf "$HOME/.config/dunst/dunstrc" &
kime &
nm-applet --indicator &
$HOME/.screenlayout/ext_main.sh &

/usr/bin/qtile start
