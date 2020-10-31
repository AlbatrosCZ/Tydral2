from Gui.pygui import Window

screen = Window(True, 0, 0)
screen.fps = 300

left_menu = [False, False]

while True:
    if screen.actions.exit_:
        break
    screen.screen.fill((0,0,0))

    if left_menu[0]:
        if not left_menu[1]:
            on = screen.draw_button([0, 0, 50, screen.height])[0]
            if on:
                left_menu[1] = True
        else:
            on = screen.draw_button([0, 0, 100, screen.height])[0]
            if not on:
                left_menu[1] = False

    on, exit_ = screen.draw_button(["r-3", 3, 0, 0], button_color=(0,0,0), text_color=(255,50,50), text = "Exit")
    if exit_:
        break

    screen.loop()

print()
print(f"EXITING: {True}")