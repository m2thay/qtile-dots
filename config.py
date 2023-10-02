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
#Imports
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
import psutil
import os
import subprocess

#Set your modkey
mod = "mod4"
#Terminal, uses "guess_terminal" by default. Doesn't really matter as opening alacritty is defined in key bindings later.
terminal = "alacritty"

#Autostart .config/qtile/autostart.sh
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


@hook.subscribe.client_new
def _swallow(window):
    pid = window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False

#Change window structure
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    #Open terminal, change to "guess_terminal" if you want it to use your terminal as defined earlier.
    Key([mod], "t", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below, doesn't really matter as I only use the "Columns" layout.
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "v", lazy.spawn("brave-browser"), desc="Open Brave"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Open application launcher"),
    Key([mod, "shift"], "l", lazy.spawn("/home/arttu/AppImages/Librewolf.AppImage"), desc="Open Librewolf"),
    Key([mod, "shift"], "d", lazy.spawn("discord"), desc="Open Discord"),
    Key([mod, "shift"], "p", lazy.spawn("lollypop"), desc="Media player"),
    Key([mod, "shift"], "c", lazy.spawn("chromium"), desc="Secondary browser"),
    Key([mod, "shift"], "y", lazy.spawn("brightnessctl s +100"), desc="Set brightness up"),
    Key([mod, "shift"], "u", lazy.spawn("brightnessctl s 100-"), desc="Set brightness down"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), desc="Mute audio"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"), desc="Sound down"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"), desc="Sound down"),
    Key([mod, "shift"], "f", lazy.spawn("firefox"), desc="Browser"),  
    Key([mod, "shift"], "n", lazy.spawn("nemo"), desc="Open graphical file browser"),  
    Key([mod, "shift"], "t", lazy.spawn("thunderbird"), desc="Open mail"),  
    Key([mod, "shift"], "g", lazy.spawn("grim"), desc="Take a screenshot"),  
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    Key([mod], "p", lazy.spawn("pavucontrol"), desc="Control volume"),
    Key([mod], "r", lazy.spawn("alacritty -e ranger"), desc="Open terminal file browser"),
    Key([mod, "shift"], "r", lazy.spawn("liferea"), desc="Open RSS reader"),
    Key([mod], "m", lazy.spawn("./Scripts/Monitorsetup"), desc="DMenu script to setup monitors"),
    Key([mod], "n", lazy.spawn("nitrogen"), desc="Change wallpaper"),
]
#Groups, tags, whatever you want to call them. Change to whatever you'd like.
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

#To set up multiple layouts, add layout.Nameoflayout( (margins, border width, etc)
layouts = [
    layout.Columns(border_width=4, margin = 2, border_focus="#"),
    layout.Max(
    border_width=2
        ),
    # Try more layouts by unleashing below layouts.
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

#Set default parameters for Widgets
widget_defaults = dict(
    font="Hack Nerd Font Bold",
    fontsize=12,
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


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0, padding=2, foreground=colors[2], background=colors[0]
                ),
                widget.Image( # Set an image of the distro logo if wanted 
                    scale=True,
                    filename="~/.config/qtile/images/penguin.png",
                    background=colors[0],
                ),
                widget.Sep(  # Separator between image and group box.
                    linewidth=0, padding=0, foreground=colors[2], background=colors[0]
                ),
                widget.GroupBox(
                    fontsize=14,
                    margin_y=3,
                    margin_x=3,
                    padding_y=5,
                    padding_x=3,
                    spacing=0,
                    center_aligned=True,
                    active=colors[8],
                    inactive=colors[8],
                    rounded=True,
                    highlight_color=colors[5],
                    highlight_method="block",
                    this_current_screen_border=colors[5],
                    this_screen_border=colors[5],
                    other_current_screen_border=colors[5],
                    other_screen_border=colors[5],
                    foreground=colors[8],
                    background=colors[0],
                ),
                # widget.Prompt( # Nah, rather use rofi or dmenu.
                # prompt=prompt,
                # font="Ubuntu",
                # padding=10,
                # foreground=colors[8],
                # background=colors[0],
                # ),
                widget.Sep(  # Separator between Groupbox and Window name.
                    linewidth=0, padding=0, foreground=colors[2], background=colors[0]
                ),
                widget.TaskList(
                    fontsize=14,
                    foreground=colors[8],
                    background=colors[0],
                    border=colors[5],
                    center_aligned=True,
                    spacing=6,
                    margin_y=5,
                    margin_x=3,
                    padding_y=0,
                    padding_x=3,
                    max_title_width=350,
                    highlight_color=colors[5],
                    highlight_method="block",
                    rounded=True,
                    icon_size=20
                ),
                widget.Sep(  # Separator between Window name and widgets.
                    linewidth=0, padding=20, foreground=colors[2], background=colors[0]
                ),
                widget.OpenWeather(
                    location='Helsinki',
                    padding=5,
                    format='{location_city}: {main_temp} °{units_temperature} {humidity}% {weather_details}',
                    foreground=colors[8],
                    background=colors[4],
                    ),
                widget.Battery(
                    padding=10,
                    foreground=colors[8],
                    background=colors[0],
                    fontsize=12,
                    discharge_char="", 
                    charge_char="",
                    format='{percent:1.0%}, {hour:d}:{min:02d} {char}'
                ),
                widget.TextBox(
                    text=" ",
                    padding=2,
                    foreground=colors[8],
                    background=colors[4],
                   fontsize=12,
                ),
                widget.ThermalSensor(
                    foreground=colors[8],
                    background=colors[4],
                    threshold=90,
                    padding=5,
                    update_interval=90
                ),
                widget.TextBox(
                    text=" ",
                    padding=2,
                    foreground=colors[8],
                    background=colors[0],
                    fontsize=14,
                ),
                widget.CPU(
                    foreground=colors[8],
                    background=colors[0],
                    padding=5,
                    update_interval=30,
                    format="{load_percent}%",
                ),
                widget.TextBox(
                    text=" ",
                    foreground=colors[8],
                    background=colors[4],
                    padding=0
                ),
                widget.Volume(
                        foreground=colors[8],
                        background=colors[4],
                        padding=5),
                #Set to your network interface to use
                # widget.Net(
                # interface = "enp7s0",
                # format="{down} ↓↑ {up}",
                # foreground=colors[8],
                # background=colors[27],
                # padding=5,
                # ),
                widget.Clock(
                    foreground=colors[8],
                    background=colors[0],
                    format=" %a, %b %d %H:%M ",
                ),
                # widget.BatteryIcon(
                    # update_interval=60, foreground=colors[8], background=colors[4]
                # ),
                widget.Systray(background=colors[4], padding=5),
                widget.Sep(
                    linewidth=0, padding=10, foreground=colors[8], background=colors[4]
                ),
                # widget.CurrentLayout(
                    # foreground=colors[8], background=colors[0], padding=5
                # ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        #Set floating rules
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

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

#Set WM name for COOL NEOFETCH!!!
wmname = "Qtile"
