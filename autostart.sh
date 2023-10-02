#!/bin/sh

picom --config .config/picom/picom.conf &
nitrogen --restore &
setxkbmap fi &
nm-applet &
dunst &
xset r rate 500 40 &
