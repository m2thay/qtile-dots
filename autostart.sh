#!/bin/sh

nitrogen --restore &
bash .mouseaccel &
bash .screenlayout/screenlayout.sh &
kanshi --config .config/kanshi/kanshi.conf &
xset r rate 500 40 &
lxsession &
dunst &
easyeffects --gapplication-service &
