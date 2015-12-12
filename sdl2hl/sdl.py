from enum import IntEnum

from sdl2._sdl2 import ffi, lib
from error import check_int_err
import enumtools


class InitFlag(IntEnum):
    """These are the flags which may be passed to SDL_Init(). You should specify the subsystems which
    you will be using in your application.
    """
    timer = lib.SDL_INIT_TIMER
    audio = lib.SDL_INIT_AUDIO
    video = lib.SDL_INIT_VIDEO
    joystick = lib.SDL_INIT_JOYSTICK
    haptic = lib.SDL_INIT_HAPTIC
    gamecontroller = lib.SDL_INIT_GAMECONTROLLER
    events = lib.SDL_INIT_EVENTS
    everything = (lib.SDL_INIT_TIMER
                  | lib.SDL_INIT_AUDIO
                  | lib.SDL_INIT_VIDEO
                  | lib.SDL_INIT_JOYSTICK
                  | lib.SDL_INIT_HAPTIC
                  | lib.SDL_INIT_GAMECONTROLLER
                  | lib.SDL_INIT_EVENTS)


def init(*flags):
    """This function initializes the subsystems specified by flags.

    Args:
        *flags (InitFlag): Flags specifying which subsystems to initialize.

    Raises:
        SDLError: If there's an error initializing SDL.
    """
    check_int_err(lib.SDL_Init(enumtools.get_mask(flags)))

def was_init():
    """This function returns the subsystems which have previously been initialized.

    Returns:
        Set[InitFlag]: Flags indicating which subsystems have been initialized.
    """
    mask = lib.SDL_WasInit(0)
    return enumtools.get_items(InitFlags, mask, {InitFlags.everything})

def quit():
    """ This function cleans up all initialized subsystems. You should call it upon all exit conditions."""

    lib.SDL_Quit()
