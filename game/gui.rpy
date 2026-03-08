## GUI Configuration

define gui.text_font = "DejaVuSans.ttf"
define gui.name_text_font = "DejaVuSans.ttf"
define gui.interface_text_font = "DejaVuSans.ttf"
define gui.text_size = 22
define gui.name_text_size = 30
define gui.interface_text_size = 22
define gui.label_text_size = 24
define gui.notify_text_size = 16
define gui.title_text_size = 50
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"
define gui.textbox_height = 185
define gui.textbox_yalign = 1.0
define gui.name_xpos = 240
define gui.name_ypos = 0
define gui.name_xalign = 0.0
define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False
define gui.dialogue_xpos = 268
define gui.dialogue_ypos = 50
define gui.dialogue_width = 744
define gui.dialogue_text_xalign = 0.0

init python:
    gui.init(1280, 720)
