export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export QT_QPA_PLATFORMTHEME=qt5ct

/usr/bin/lxqt-policykit-agent &
dunst -conf "$HOME/.config/dunst/dunstrc" &
fcitx5 &
nm-applet &
blueman-applet &
$HOME/.screenlayout/ext_main.sh &

/usr/bin/qtile start
