from sdl2._sdl2 import lib


def get_ticks():
    """Get the number of milliseconds since the SDL library initialization.

    Returns:
        int: The number of milliseconds since the SDL library initialization.
    """
    return lib.SDL_GetTicks()

def get_performance_counter():
    """Get the current value of the high resolution counter.

    Returns:
        long: The current value of the high resolution counter.
    """
    return lib.SDL_GetPerformanceCounter()

def get_performance_frequency():
    """Get the count per second of the high resolution counter.

    Returns:
        long: The count per second of the high resolution counter.
    """
    return lib.SDL_GetPerformanceFrequency()

def delay(ms):
    """Wait a specified number of milliseconds before returning.

    Args:
        ms (int): The number of milliseconds to wait.
    """
    lib.SDL_Delay(ms)
