from sdl2._sdl2 import lib

for name in dir(lib):
    if name.startswith("SDL_") and isinstance(getattr(lib, name), int):
        globals()[name[4:]] = getattr(lib, name)
    elif name.startswith("SDL") and isinstance(getattr(lib, name), int):
        globals()[name[3:]] = getattr(lib, name)
