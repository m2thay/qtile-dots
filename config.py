#              _   _   _                    ___  _   _ _
# _ __ ___    / \ | |_| |__   __ _ _   _   / _ \| |_(_) | ___
#| '_ ` _ \  / _ \| __| '_ \ / _` | | | | | | | | __| | |/ _ \
#| | | | | |/ ___ \ |_| | | | (_| | |_| | | |_| | |_| | |  __/
#|_| |_| |_/_/   \_\__|_| |_|\__,_|\__, |  \__\_\\__|_|_|\___|
#                                  |___/
# ____        _
#|  _ \  ___ | |_ ___
#| | | |/ _ \| __/ __|
#| |_| | (_) | |_\__ \
#|____/ \___/ \__|___/
#
# Imports
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig

import os
import subprocess
import psutil

#Set modkey (Super)
mod = "mod4"
#Terminal, uses "guess_terminal" by default, remember to import!
myTerm = "alacritty"
#Set browser variable
myBrowser = "firefox"

#Set startup applications in .config/qtile/autostart.sh
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

#Qtile related keybindings (lots more available, these are just the ones I use)
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
#Various other keybindings, change to preference. These are quite arbitrary and just something I've gotten used to.
    Key([mod], "t", lazy.spawn(myTerm), desc="Launch terminal"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Open application launcher"),
    Key([mod], "b", lazy.spawn("strawberry"), desc="Media player"),
    Key([mod], "c", lazy.spawn("chromium"), desc="Secondary browser"),
    Key([mod, "shift"], "y", lazy.spawn("brightnessctl s +100"), desc="Set brightness up"),
    Key([mod, "shift"], "u", lazy.spawn("brightnessctl s 100-"), desc="Set brightness down"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), desc="Mute audio"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"), desc="Sound down"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"), desc="Sound down"),
    Key([mod], "w", lazy.spawn("firefox"), desc="Browser"),  
    Key([mod], "n", lazy.spawn("nemo"), desc="Open graphical file browser"),  
    Key([mod, "shift"], "t", lazy.spawn("thunderbird"), desc="Open mail"),  
    Key([mod], "g", lazy.spawn("grim"), desc="Take a screenshot"),  
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    Key([mod], "p", lazy.spawn("pavucontrol"), desc="Control volume"),
    Key([mod], "r", lazy.spawn("liferea"), desc="Open RSS reader"),
    Key([mod], "m", lazy.spawn("bash .mouseaccel"), desc="Setup mice"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next track"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key([mod], "space", lazy.spawn("playerctl play-pause"), desc="Play/Pause"),
    Key([mod], "e", lazy.spawn("easyeffects"), desc="Change EQ settings"),
    Key([mod], "s", lazy.spawn("steam-native"), desc="Change EQ settings"),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    Key([mod], "o", lazy.spawn("obs"), desc="Start streaming/recording"),
    Key([mod], "m", lazy.spawn("./Scripts/displayselect"), desc="Change monitor setup"),
    Key([mod], "a", lazy.spawn("arandr"), desc="Change monitor setup"),
]

#Add groups here, also use asdfuiop if want be. 
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

#Configure layouts, I prefer Columns or MonadTall, but feel free to use any of the ones listed below 
layouts = [
    layout.Columns(border_width=4,
        margin = 10,
        border_focus="#cc241d",
        border_on_single=0,
        margin_on_single=0,
        ),
    layout.Max(
    border_width=2
        ),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

#Set the default settings for different widgets
widget_defaults = dict(
    font="Hack Nerd Font Bold",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()
#Set gruvbox colors
colors = [
    ["#282828", "#282828"],  # 0  # bg
    ["#282828", "#282828"],  # 1  # bg0
    ["#1d2021", "#1d2021"],  # 2  # bg0_h
    ["#32302f", "#32302f"],  # 3  # bg0_s
    ["#3c3836", "#3c3836"],  # 4  # bg1
    ["#504945", "#504945"],  # 5  # bg2
    ["#665c54", "#665c54"],  # 6  # bg3
    ["#7c6f64", "#7c6f64"],  # 7  # bg4
    ["#ebdbb2", "#ebdbb2"],  # 8  # fg
    ["#fbf1c7", "#fbf1c7"],  # 9  # fg0
    ["#ebdbb2", "#ebdbb2"],  # 10 # fg1
    ["#d5c4a1", "#d5c4a1"],  # 11 # fg2
    ["#bdae93", "#bdae93"],  # 12 # fg3
    ["#a89984", "#a89984"],  # 13 # fg4
    ["#cc241d", "#cc241d"],  # 14 # red hard
    ["#fb4934", "#fb4934"],  # 15 # red soft
    ["#98971a", "#98971a"],  # 16 # green hard
    ["#b8bb26", "#b8bb26"],  # 17 # green soft
    ["#d79921", "#d79921"],  # 18 # yellow hard
    ["#fabd2f", "#fabd2f"],  # 19 # yellow soft
    ["#458588", "#458588"],  # 20 # blue hard
    ["#83a598", "#83a598"],  # 21 # blue soft
    ["#b16286", "#b16286"],  # 22 # purple hard
    ["#d3869b", "#d3869b"],  # 23 # purple soft
    ["#689d6a", "#689d6a"],  # 24 # aqua hard
    ["#8ec07c", "#8ec07c"],  # 25 # aqua soft
    ["#d65d0e", "#d65d0e"],  # 26 # orange hard
    ["#FE8019", "#FE8019"],  # 27 # orange soft
    ["#a89984", "#a89984"],  # 28 # gray
    ["#928374", "#928374"],  # 29 # gray bg
]  # window name#


#Configure the bar
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=2,
                    foreground=colors[2],
                    background=colors[0]
                ),
                widget.Image( #Set a picture in your top left corner
                    scale=True,
#                    filename='~/.config/qtile/images/image_proxy.png',
                    background=colors[0],
                    margin=3,
                ),
                widget.Sep(  # Separator between image and group box.
                    linewidth=0,
                    padding=0,
                    foreground=colors[2],
                    background=colors[0]
                ),
                widget.GroupBox(
                    margin_y=3,
                    margin_x=3,
                    padding_y=3,
                    padding_x=3,
                    spacing=0,
                    center_aligned=True,
                    active=colors[8],
                    inactive=colors[7],
                    rounded=True,
                    highlight_color=colors[5],
                    highlight_method='line',
                    this_current_screen_border=colors[24],
                    this_screen_border=colors[5],
                    other_current_screen_border=colors[5],
                    other_screen_border=colors[5],
                    foreground=colors[8],
                    background=colors[0],
                    disable_drag=True,
                    toggle=False,
                    use_mouse_wheel=False,
                    mouse_callbacks={'Button1': lambda: None}
                ),
                widget.WindowName(
                    foreground=colors[8],
                    background=colors[0],
                    max_chars=20,
                    scroll=True,
                ),
                widget.KeyboardLayout(
                    background=colors[0],
                    foreground=colors[8],
                    configured_keyboards=['us', 'fi']
                ),
                widget.OpenWeather(
                    location='Helsinki', #Set your own city here
                    foreground=colors[8],
                    background=colors[4],
                    format='{location_city}: {main_temp}°{units_temperature} {weather_details} {icon}',
                    update_interval=600,
                    padding=5

                ),
                widget.Clock(
                    foreground=colors[8],
                    background=colors[0],
                    format=" %a, %b %d %H:%M ",
                ),
                widget.Systray(
                    background=colors[4],
                    padding=3
                    ),
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]



#Set keyboard rules under the Qtile's Wayland wlroots implementation
wl_input_rules = {
        'type:pointer':
        InputConfig(
        accel_profile='flat', pointer_accel=0
        ),
        'type:keyboard': InputConfig(
        kb_repeat_rate=50,
        kb_repeat_delay=400),
}


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing focus, should we respect this or not?
auto_minimize = False

#Set WM name for epic Neofetch
wmname = "Qtile"
