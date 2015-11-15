from sdl2._sdl2 import lib


def get_ticks():
    return lib.SDL_GetTicks()

def get_performance_counter():
    return lib.SDL_GetPerformanceCounter()

def get_performance_counter_hz():
    return lib.SDL_GetPerformanceFrequency()

def delay(ms):
    lib.SDL_Delay(ms)
