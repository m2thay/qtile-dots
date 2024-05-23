#!/bin/sh

nitrogen --restore &
xrandr --rate 240 &
bash .mouseaccel &
xset r rate 500 40 &
lxsession &
picom &
dunst &
redshift -P -O 5000 &
easyeffects --gapplication-service &
swaybg -o eDP-1 -i /mnt/28261aa5-ca0c-46a9-820b-2ac7b17f093e/Pictures/boomerlarpswoods.png 
xinput disable "Synaptics TM3276-022"
