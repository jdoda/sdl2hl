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
        
    def draw_arc(self, x, y, r, start, end, color):
        """Draw an arc.
        
        Args:
            x (int): The x coordinate of the center of the arc.
            y (int): The y coordinate of the center of the arc.
            r (int): The radius of the arc.
            start (int): The start of the arc.
            end (int): The end of the arc.
            color (Tuple[int, int, int, int]): The color of the circle.
            
        Raises:
            SDLError: If an error is encountered.
        """
        check_int_err(lib.arcRGBA(self._ptr, x, y, r, start, end, color[0], color[1], color[2], color[3]))

    def draw_line(self, x1, y1, x2, y2, color):
        """Draw a line.

        Args:
            x1 (int): The x coordinate of the start of the line.
            y1 (int): The y coordinate of the start of the line.
            x2 (int): The x coordinate of the end of the line.
            y2 (int): The y coordinate of the end of the line.
            color (Tuple[int, int, int, int]): The color of the circle.

        Raises:
            SDLError: If an error is encountered.

        """
        check_int_err(lib.lineRGBA(self._ptr, x1, y1, x2, y2, color[0], color[1], color[2], color[3]))
