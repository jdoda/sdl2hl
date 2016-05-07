from enum import IntEnum

from sdl2._sdl2 import lib
from error import check_int_err, check_ptr_err


class ControllerAxis(IntEnum):
    invalid = lib.SDL_CONTROLLER_AXIS_INVALID
    leftx = lib.SDL_CONTROLLER_AXIS_LEFTX
    lefty = lib.SDL_CONTROLLER_AXIS_LEFTY
    rightx = lib.SDL_CONTROLLER_AXIS_RIGHTX
    righty = lib.SDL_CONTROLLER_AXIS_RIGHTY
    triggerleft = lib.SDL_CONTROLLER_AXIS_TRIGGERLEFT
    triggerright = lib.SDL_CONTROLLER_AXIS_TRIGGERRIGHT
    max = lib.SDL_CONTROLLER_AXIS_MAX

    
class ControllerButton(IntEnum):
    invalid = lib.SDL_CONTROLLER_BUTTON_INVALID
    a = lib.SDL_CONTROLLER_BUTTON_A
    b = lib.SDL_CONTROLLER_BUTTON_B
    back = lib.SDL_CONTROLLER_BUTTON_BACK
    dpad_down = lib.SDL_CONTROLLER_BUTTON_DPAD_DOWN
    dpad_left = lib.SDL_CONTROLLER_BUTTON_DPAD_LEFT
    dpad_right = lib.SDL_CONTROLLER_BUTTON_DPAD_RIGHT
    dpad_up = lib.SDL_CONTROLLER_BUTTON_DPAD_UP
    guide = lib.SDL_CONTROLLER_BUTTON_GUIDE
    leftshoulder = lib.SDL_CONTROLLER_BUTTON_LEFTSHOULDER
    leftstick = lib.SDL_CONTROLLER_BUTTON_LEFTSTICK
    rightshoulder = lib.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER
    rightstick = lib.SDL_CONTROLLER_BUTTON_RIGHTSTICK
    start = lib.SDL_CONTROLLER_BUTTON_START
    x = lib.SDL_CONTROLLER_BUTTON_X
    y = lib.SDL_CONTROLLER_BUTTON_Y
    max = lib.SDL_CONTROLLER_BUTTON_MAX
    

class GameController(object):
    
    @staticmethod
    def get_count():
        return check_int_err(lib.SDL_NumJoysticks())
    
    def __init__(self, index=0):
        self._ptr = check_ptr_err(lib.SDL_GameControllerOpen(index))
        
    def __del__(self):
        check_ptr_err(lib.SDL_GameControllerClose(self._ptr))
        
    def get_axis(self, axis):
        return lib.SDL_GameControllerGetAxis(self._ptr, axis)
        
    def get_button(self, button):
        return bool(lib.SDL_GameControllerGetButton(self._ptr, button))
        
    

