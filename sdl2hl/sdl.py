from sdl2._sdl2 import ffi, lib
from error import check_int_err


def init(flags=0):
    check_int_err(lib.SDL_Init(flags))
#     lib.Mix_Init(lib.MIX_INIT_OGG)
#     lib.Mix_OpenAudio(44100, lib.MIX_DEFAULT_FORMAT, lib.MIX_DEFAULT_CHANNELS, 1024)
#     lib.TTF_Init()

def quit():
#     lib.TTF_Quit()
#     lib.Mix_Quit()
    lib.SDL_Quit()
