## This file contains options that can be changed to customize your game.

define config.name = _("Bohemian Steam Chic - Prototype")
define gui.show_name = True
define config.version = "0.1"
define gui.about = _("")
define build.name = "BohemianSteamChic"
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)
default preferences.text_cps = 40
default preferences.afm_time = 15
define config.save_directory = "BohemianSteamChic-1"
define config.window_icon = "gui/window_icon.png"

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.rpy', None)
    build.classify('**.rpyc', 'archive')
    build.documentation('*.html')
    build.documentation('*.txt')
