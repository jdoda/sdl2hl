from sdl2._sdl2 import ffi, lib
from error import check_int_err, check_ptr_err
from surface import Surface


class Font(object):

    @staticmethod
    def from_path(path, size):
        font = object.__new__(Font)
        font._ptr = check_ptr_err(lib.TTF_OpenFont(path, size))
        return font
    
    def __init__(self, font_bytes, size):
        self._bytes = font_bytes # This is a workaround for some sort of weird lifetime issue.
        rw = check_ptr_err(lib.SDL_RWFromConstMem(self._bytes, len(self._bytes)))
        self._ptr = check_ptr_err(lib.TTF_OpenFontRW(rw, 1, size))
        
    def __del__(self):
        lib.TTF_CloseFont(self._ptr)
        
    def render_solid(self, text, color):
        return Surface._from_ptr(check_ptr_err(lib.TTF_RenderUTF8_Solid(self._ptr, text.encode('utf-8'), color)))
        
    def render_blended(self, text, color):
        return Surface._from_ptr(check_ptr_err(lib.TTF_RenderUTF8_Blended(self._ptr, text.encode('utf-8'), color)))
        

def init():
    check_int_err(lib.TTF_Init())
    
def quit():
    lib.TTF_Quit()
        
