from sdl2._sdl2 import ffi, lib
from error import check_int_err


def init(flags=0):
    """This function initializes the subsystems specified by flags.

    Args:
        flags: Flags specifying which subsystems to initialize.

    Raises:
        SDLError: If there's an error initializing SDL.
    """
    check_int_err(lib.SDL_Init(flags))

def quit():
    """ This function cleans up all initialized subsystems. You should call it upon all exit conditions."""

    lib.SDL_Quit()
