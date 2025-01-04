## Display Chord Options
from libqtile.widget import base
from libqtile.lazy import LazyCall
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, send_notification
from os.path import expanduser, expandvars
import os
import subprocess
import qtile_extras

from qtile_extras.popup.toolkit import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)

from qtile_extras.widget.decorations import PowerLineDecoration

powerline = {
    "decorations": [
        PowerLineDecoration()
    ]
}




class ChordOptions(base._TextBox):
    """Display possible modes"""
    defaults = [
        (
            "chords_colors",
            {},
            "colors per chord in form of tuple {'chord_name': ('bg', 'fg')}. "
            "Where a chord name is not in the dictionary, the default ``background`` and ``foreground``"
            " values will be used.",
        ),
        (
            "name_transform",
            lambda txt: txt,
            "preprocessor for chord name it is pure function string -> string",
        ),
    ]

    def __init__(self, mapping, width=bar.CALCULATED, **config):
        base._TextBox.__init__(self, "", width, **config)
        self.add_defaults(ChordOptions.defaults)
        self.mapping = mapping

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        self.default_background = self.background
        self.default_foreground = self.foreground
        self.text = ""
        self._setup_hooks()

    def _setup_hooks(self):
        def hook_enter_chord(chord_name):
            # if chord_name is True:
            #     self.text = ""
            #     self.reset_colours()
            #     return

            self.text = ' '.join([f"{shortcut}:{description}" for shortcut, description in self.mapping[chord_name]] )
            lazy.spawn(f"rofi -e hallo")
            if chord_name in self.chords_colors:
                (self.background, self.foreground) = self.chords_colors.get(chord_name)
            else:
                self.reset_colours()

            self.bar.draw()

        hook.subscribe.enter_chord(hook_enter_chord)
        hook.subscribe.leave_chord(self.clear)

    def reset_colours(self):
        self.background = self.default_background
        self.foreground = self.default_foreground

    def clear(self, *args):
        self.reset_colours()
        self.text = ""
        self.bar.draw()


mod = "mod4"
terminal = guess_terminal()

@hook.subscribe.startup_once
def startup_once():
    script = expandvars("$TOBI_ENV/autostart.sh")
    subprocess.call([script])
    return

def ungrabchords(func):
    def wrapped_function(qtile):
        func(qtile)
        qtile.ungrab_all_chords()
        return 
    return wrapped_function

# config_keychords = {
    # "key": "space",
    # "desc": "custom bindings",
    # "func": lazy.function(ungrabchords(open_menu))
    # "mode": "custom",
    # "options": [
    #     {
    #         "key": "r",
    #         "desc": "renameWindow",
    #         "func": lazy.function(ungrabchords(rename_window)), 
    #     },
    #     {
    #         "key": "s",
    #         "desc": "switchWindow",
    #         "func": lazy.function(ungrabchords(change_window)), 
    #     },
    #     {
    #         "key": "u",
    #         "desc": "ui",
    #         "mode": "ui",
    #         "options": [
    #             {
    #                 "key": "w",
    #                 "desc": "changeWallpaper",
    #                 "func": lazy.function(ungrabchords(change_wallpaper))
    #             }
    #         ]
    #     }
    # ]
#}

mode_key_mapping = {}

def get_key_options(key_options):
    if isinstance(key_options, dict):
        # oooh we need to have a keychord
        # with the options as keys
        mode = key_options.get("mode", None)
        if not mode:
            return Key(
                [], 
                key_options["key"], 
                key_options["func"],
                desc=key_options["desc"],
                swallow=True
            )

        sub_options = get_key_options(key_options["options"])
        usable_keys = [(option.key, option.desc) for option in sub_options]
        mode_key_mapping[mode] = usable_keys

        return KeyChord(
            modifiers=[], 
            key=key_options["key"],
            submappings=sub_options,
            mode=False,
            name=key_options["mode"],
            desc=key_options["desc"],
            swallow=True
        )

    return [
        get_key_options(option) 
        for option in key_options 
    ]


#custom_key_config  = get_key_options(config_keychords)
#custom_key_config.modifiers = [mod]

keys = [
     # custom_key_config,
    # open menu
    Key([mod], "space", 
        lazy.spawn(
            expandvars("$TOBI_ENV/Menu"), 
            shell=True
        ), 
        desc="Open Menu"),

    Key([mod], "w", 
        lazy.spawn(
            expandvars("$TOBI_ENV/WindowSwitch"), 
            shell=True
        ), 
        desc="Open Menu"),


    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Move windows 
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows
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

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "x", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "b", lazy.hide_show_bar(), desc="Hides the bar"),

    # Toggle fullscreen
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
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

groups = [
        Group(name="1", screen_affinity=0),
        Group(name="2", screen_affinity=0),
        Group(name="3", screen_affinity=0),
        Group(name="4", screen_affinity=0),
        Group(name="5", screen_affinity=0),
        Group(name="6", screen_affinity=0),
        Group(name="7", screen_affinity=0),
        Group(name="8", screen_affinity=0),
        Group(name="9", screen_affinity=1),
]

def go_to_group(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].toscreen()
            return
        if name in '12345678':
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()
        else:
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

    return _inner

for i in groups:
    keys.append(Key([mod], i.name, lazy.function(go_to_group(i.name))))

def go_to_group_and_move_window(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.togroup(name, switch_group=True)
            return
        if name in "12345678":
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()
        elif name == '9':
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()

    return _inner

# setup keys switching groups
for i in groups:
    keys.append(
            Key([mod], 
                i.name, 
                lazy.function(
                    go_to_group(i.name)
                )
            )
    )

# setup keys for moving windows
for i in groups:
    keys.append(
            Key([mod, "shift"], 
                i.name, 
                lazy.function(
                    go_to_group_and_move_window(i.name)
                )
            )
    )



layouts = [
    layout.Columns(
        border_width=4,
        border_focus="#999999",
        border_normal="#222222",
        margin=[3, 3, 3, 3],
    ),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(top=bar.Bar(
            [
                qtile_extras.widget.CurrentLayoutIcon(
                    background="000000", 
                    **powerline
                ),
                qtile_extras.widget.GroupBox(
                    background="111111",
                    **powerline
                ),
                qtile_extras.widget.WindowName(
                    background="222222", 
                    **powerline
                ),
                qtile_extras.widget.Clock(
                    background="444444", 
                    format='%y/%m/%d %H:%M',
                    **powerline
                ),
                qtile_extras.widget.QuickExit(
                    background="666666",
                    default_text="&#9212;"
                )
            ],
            20,
            background="225522"
    )),
    Screen(top=bar.Bar(
            [
                qtile_extras.widget.CurrentLayoutIcon(background="000000", **powerline),
                qtile_extras.widget.GroupBox(
                    background="111111",
                    **powerline
                ),
                qtile_extras.widget.WindowName(background="222222", **powerline),
                qtile_extras.widget.Clock(background="444444", **powerline),
                qtile_extras.widget.QuickExit(
                    background="666666",
                    default_text="&#9212;"
                )
            ],
            20,
    ))
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
floats_kept_above = True
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

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"




