import sys

import sdl2hl


BACKGROUND_COLOR = (0,0,0,255)
AVATAR_COLOR = (255,0,0,255)


sdl2hl.init()
window = sdl2hl.Window()
renderer = sdl2hl.Renderer(window)
avatar = sdl2hl.Rect(w=64, h=64)

while True:
    for event in sdl2hl.events.poll():
        if event.type == sdl2hl.QUIT:
            sdl2hl.quit()
            sys.exit()
        elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_LEFT:
            avatar.x -= 1
        elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_RIGHT:
            avatar.x += 1
        elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_UP:
            avatar.y -= 1
        elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_DOWN:
            avatar.y += 1

    renderer.draw_color = BACKGROUND_COLOR
    renderer.clear()
    renderer.draw_color = AVATAR_COLOR
    renderer.fill_rect(avatar)

    renderer.present()
    
