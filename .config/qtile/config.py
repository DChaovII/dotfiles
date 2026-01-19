# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from math import ceil
import libqtile.resources

from qtile_extras import widget as extra_widget

from libqtile import bar, layout, qtile, hook, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig
# from libqtile.utils import guess_terminal
import colours


#@hook.subscribe.startup_once
#def autostart():
#    home = os.path.expanduser('~/.config/qtile/autostart.sh')
#    subprocess.call(home)

#@hook.subscribe.client_new
#def bring_to_front(client):
#    if client.floating:
#        client.bring_to_front()
#        client.focus()

@hook.subscribe.client_new
def handle_kakaotalk(client):
    wm_class = client.get_wm_class()
    if wm_class and 'kakaotalk.exe' in wm_class:
        if client.name != "카카오톡":
            client.can_steal_focus = False
            client.togroup(qtile.current_group.name)

def is_hdmi_connected():
    try:
        output = subprocess.check_output("xrandr").decode("utf-8")
        return "HDMI-1 connected" in output
    except Exception:
        return False

mod = "mod1" # mod4 == Super_L, mod1 == Alt_L
#myTerminal = guess_terminal()
myTerminal = 'alacritty'
myBrowser = 'brave'
myFm = 'pcmanfm-qt'
myWall = '~/.config/qtile/wallpaper/wallpaper.jpg'
colours = colours.nord

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "j", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "l", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.next_screen(), desc="Move focus to next screen"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    #Key([mod, "control"], "h", lazy.layout.shrink(), desc="Shrink mai pane"),
    #Key([mod, "control"], "l", lazy.layout.grow(), desc="Grow main pane"),
    Key([mod, "control"], "j", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "control"], "k", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod, "control"], "n", lazy.layout.reset(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(myTerminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "p", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod, "shift"], "q", lazy.spawn('rofi -show p -modi p:rofi-power-menu'), desc="Spawn rofi power meno"),
    #Key([mod], "p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "p", lazy.spawn('rofi -show drun -show-icons'), desc="Spawn a rofi launcher"),

    Key([mod, "shift"], "e", lazy.spawn(myBrowser), desc="Spawn my web browser"),
    Key([mod], "e", lazy.spawn(myFm), desc="Spawn my gui file manager"),

    Key([mod], "Escape", lazy.spawn("rofi -show p -modi p:rofi-power-menu"), desc="Spawn rofi power menu"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 2"), desc="Raise volume by 2%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 2"), desc="Lower volume by 2%"),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="Toggle mute volume"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brillo -A 5"), desc="Increase brightness by 5%"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brillo -U 5"), desc="Decrease brightness by 5%"),
Key([mod, "shift"], "o", lazy.spawn(os.path.expanduser("~/.config/qtile/screenshotScripts/maimSelect.sh")), desc="Screenshot selected region with maim"), # mod-shift-o == PrtSc without Fn
    Key([], "Print", lazy.spawn(os.path.expanduser("~/.config/qtile/screenshotScripts/maimFull.sh")), desc="Screenshot selected screen with maim"), # Fn+PrtSc == PrtSc
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

#group_len = 7
#group_names = [str(i+1) for i in range(group_len)]
#group_labels = ['DEV', 'WEB', 'SYS', 'DOC', 'MUS', 'BOOK', 'MISC']
#groups = [Group(name=group_names[i], label=group_labels[i]) for i in range(group_len-1)]+[Group(name=group_names[-1], label=group_labels[-1], matches=[Match(title='카카오톡')])]
groups = [Group(name=i, label=f' {i} ') for i in '1234']
groups.append(
        Group(
            name = "5",
            label = ' 5 ',
            matches=[Match(title='카카오톡', wm_class='kakaotalk.exe')]
            )
        )

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
        "border_width": 2,
        "margin": 8,
        'border_focus':colours[2][1],
        'border_normal':colours[0][0]
        }

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

default_myPad=8
default_fontsize=15
default_padding=3
default_spacer=5
default_barsize=28
widget_defaults = dict(
        font="Mononoki Nerd Font Bold",
        fontsize=default_fontsize,
        padding=default_padding,
        background=colours[0][0],
        foreground=colours[1][2],
)
extension_defaults = widget_defaults.copy()

# scaling
scale = 1.2
myPad_scaled=ceil(default_myPad*scale)
fontsize_scaled=ceil(default_fontsize*scale)
padding_scaled=ceil(default_padding*scale)
spacer_scaled=ceil(default_spacer*scale)
barsize_scaled=ceil(default_barsize*scale)

# apply proper scaling
if is_hdmi_connected():
    #bar0
    myPad0=default_myPad
    fontsize0=default_fontsize
    padding0=default_padding
    spacer0=default_spacer
    barsize0=default_barsize
    #bar1
    myPad1=myPad_scaled
    fontsize1=fontsize_scaled
    padding1=padding_scaled
    spacer1=spacer_scaled
    barsize1=barsize_scaled
else:
    #bar0
    myPad0=myPad_scaled
    fontsize0=fontsize_scaled
    padding0=padding_scaled
    spacer0=spacer_scaled
    barsize0=barsize_scaled
    #bar1
    myPad1=default_myPad
    fontsize1=default_fontsize
    padding1=default_padding
    spacer1=default_spacer
    barsize1=default_barsize

bar0 = bar.Bar(
            [
                #widget.QuickExit(
                #    default_text='',
                #    countdown_format='{}',
                #    padding=10,
                #    fontsize=18,
                #    ),
                widget.GroupBox(
                    fontsize=fontsize0,
                    padding=padding0,
                    highlight_method = 'line',
                    highlight_color = [colours[0][1], colours[0][1]],
                    active = colours[1][2],
                    inactive = colours[0][3],
                    this_current_screen_border = colours[2][1],
                    this_screen_border = colours[3][3],
                    other_current_screen_border = colours[2][1],
                    other_screen_border = colours[3][3],
                    urgent_border = colours[3][0],
                    ),
                widget.TextBox(
                    "|",
                    fontsize=fontsize0,
                    padding=padding0,
                    ),
                widget.CurrentLayout(
                    fontsize=fontsize0,
                    padding=padding0,
                    ),
                widget.TextBox(
                    "|",
                    fontsize=fontsize0,
                    padding=padding0,
                    ),
                widget.WindowName(
                    fontsize=fontsize0,
                    padding=padding0,
                    ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                #widget.CPU(
                #    format='CPU {load_percent}%',
                #    padding=myPad_120,
                #    fontsize=fontsize_120,
                #    ),
                #widget.Memory(
                #    format='MEM {MemPercent}%',
                #    padding=myPad_120,
                #    fontsize=fontsize_120,
                #    ),
                widget.Volume(
                    #emoji=True,
                    #emoji_list=['󰝟','󰕿','󰖀','󰕾'],
                    mute_format='󰝟 MM',
                    unmute_format='󰕾 {volume}%',
                    check_mute_command='pamixer --get-mute',
                    get_volume_command='pamixer --get-volume-human',
                    padding=myPad0,
                    fontsize=fontsize0,
                    ),
                widget.Backlight(
                    backlight_name='amdgpu_bl1',
                    fmt='󰃟 {}',
                    padding=myPad0,
                    fontsize=fontsize0,
                    ),
                widget.Spacer(length=spacer0), #6
                widget.Battery(
                    format='{char} {percent:0.0%}',
                    charge_controller=lambda: (0,90),
                    empty_char='󰂎',
                    full_char='󰁹',
                    discharge_char='󰁿',
                    charge_char='󰂉',
                    not_charging_char='󱞜',
                    padding=padding0,
                    fontsize=fontsize0,
                    #padding=myPad_120,
                    ),
                widget.Systray(padding=myPad0),
                #extra_widget.StatusNotifier(padding=myPad_120),
                widget.Clock(format="%a %d %b %H:%M", padding=myPad0, fontsize=fontsize0),
                widget.Spacer(length=spacer0), #10
            ],
            size = barsize0, #34
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        )

bar1 = bar.Bar(
            [
                #widget.QuickExit(
                #    default_text='',
                #    countdown_format='{}',
                #    padding=10,
                #    fontsize=18,
                #    ),
                widget.GroupBox(
                    fontsize=fontsize1,
                    padding=padding1,
                    highlight_method = 'line',
                    highlight_color = [colours[0][1], colours[0][1]],
                    active = colours[1][2],
                    inactive = colours[0][3],
                    this_current_screen_border = colours[2][1],
                    this_screen_border = colours[3][3],
                    other_current_screen_border = colours[2][1],
                    other_screen_border = colours[3][3],
                    urgent_border = colours[3][0],
                    ),
                widget.TextBox(
                    "|",
                    fontsize=fontsize1,
                    padding=padding1,
                    ),
                widget.CurrentLayout(
                    fontsize=fontsize1,
                    padding=padding1,
                    ),
                widget.TextBox(
                    "|",
                    fontsize=fontsize1,
                    padding=padding1,
                    ),
                widget.WindowName(
                    fontsize=fontsize1,
                    padding=padding1,
                    ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                #widget.CPU(
                #    format='CPU {load_percent}%',
                #    padding=myPad,
                #    ),
                #widget.Memory(
                #    format='MEM {MemPercent}%',
                #    padding=myPad,
                #    ),
                widget.Volume(
                    #emoji=True,
                    #emoji_list=['󰝟','󰕿','󰖀','󰕾'],
                    mute_format='󰝟 MM',
                    unmute_format='󰕾 {volume}%',
                    check_mute_command='pamixer --get-mute',
                    get_volume_command='pamixer --get-volume-human',
                    padding=myPad1,
                    fontsize=fontsize1,
                    ),
                widget.Backlight(
                    backlight_name='amdgpu_bl1',
                    fmt='󰃟 {}',
                    padding=myPad1,
                    fontsize=fontsize1,
                    ),
                #widget.Spacer(length=5),
                widget.Battery(
                    format='{char} {percent:0.0%}',
                    charge_controller=lambda: (0,90),
                    empty_char='󰂎',
                    full_char='󰁹',
                    discharge_char='󰁿',
                    charge_char='󰂉',
                    not_charging_char='󱞜',
                    padding=myPad1,
                    fontsize=fontsize1,
                    ),
                #widget.Systray(padding=myPad),
                #extra_widget.StatusNotifier(padding=myPad),
                #widget.Spacer(length=5),
                widget.Clock(format="%a %d %b %H:%M", padding=myPad1, fontsize=fontsize1),
                widget.Spacer(length=spacer1),
            ],
            size = barsize1,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        )

screens = [
    Screen(
        top=bar0,
        background="#000000",
        wallpaper=myWall,
        wallpaper_mode="fill",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar1,
        background="#000000",
        wallpaper=myWall,
        wallpaper_mode="fill",
    )
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
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=2,
    border_focus=colours[2][1],
    border_normal=colours[0][0],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class='blueman-manager'),
        Match(wm_class='qalculate-gtk'),
        Match(wm_class='kakaotalk.exe'),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
#wl_input_rules = {
#        "type:keyboard": InputConfig(kb_layout='us', kb_variant='dvorak'),
#}

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
