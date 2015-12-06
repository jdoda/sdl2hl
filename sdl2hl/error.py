from sdl2._sdl2 import ffi, lib


class SDLError(Exception):
    pass


def check_int_err(int_return_value):
    if int_return_value >= 0:
        return int_return_value
    else:
        error_message = ffi.string(lib.SDL_GetError())
        lib.SDL_ClearError()
        raise SDLError(error_message)

def check_ptr_err(ptr_return_value):
    if ptr_return_value != ffi.NULL:
        return ptr_return_value
    else:
        error_message = ffi.string(lib.SDL_GetError())
        lib.SDL_ClearError()
        raise SDLError(error_message)
