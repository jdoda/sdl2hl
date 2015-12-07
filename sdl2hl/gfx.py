from sdl2._sdl2 import lib
from error import check_int_err


class GfxPrimitives(object):

    def __init__(self, renderer):
        """Create a new GfxPrimitives that draws to the given renderer.
        
        Args:
            renderer (Renderer): The renderer to draw to.
        """
        self._ptr = renderer._ptr
        
    def draw_circle(self, x, y, r, color):
        """Draw a circle.
        
        Args:
            x (int): The x coordinate of the center of the circle.
            y (int): The y coordinate of the center of the circle.
            r (int): The radius of the circle.
            color (Tuple[int, int, int, int]): The color of the circle.
            
        Raises:
            SDLError: If an error is encountered.
        """
        check_int_err(lib.circleRGBA(self._ptr, x, y, r, color[0], color[1], color[2], color[3]))
