from sdl2._sdl2 import ffi, lib


class Point(object):
    """A point on a 2D plane."""

    def __init__(self, x=0, y=0):
        """Construct a new point.

        Args:
            x (int): The x position of the point.
            y (int): The y position of the point.
        """
        self._ptr = ffi.new('SDL_Point *', [x, y])

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    @property
    def x(self):
        """int: The x position of the point."""
        return self._ptr.x

    @x.setter
    def x(self, value):
        self._ptr.x = value

    @property
    def y(self):
        """int: The y position of the point."""
        return self._ptr.y

    @y.setter
    def y(self, value):
        self._ptr.y = value


class Rect(object):
    """A rectangle, with the origin at the upper left."""

    @staticmethod
    def enclose_points(points, clip_rect):
        """Return the minimal rectangle enclosing the given set of points

        Args:
            points (List[Point]): The set of points that the new Rect must enclose.
            clip_rect (Rect): A clipping Rect.

        Returns:
            Rect: A new Rect enclosing the given points.
        """
        point_array = ffi.new('SDL_Point[]', len(points))
        for i, p in enumerate(points):
            point_array[i] = p._ptr
        enclosing_rect = Rect()
        if lib.SDL_EnclosePoints(point_array, len(points), clip_rect._ptr, enclosing_rect._ptr):
            return enclosing_rect
        else:
            return None

    def __init__(self, x=0, y=0, w=0, h=0):
        """Construct a new Rect with the given position and size.

        Args:
            x (int): The x position of the upper left corner of the rectangle.
            y (int): The y position of the upper left corner of the rectangle.
            w (int): The width of the rectangle.
            h (int): The height of the rectangle.
        """
        self._ptr = ffi.new('SDL_Rect *', [x, y, w, h])

    def __eq__(self, other):
        return bool(isinstance(other, Rect) and lib.RectEquals(self._ptr, other._ptr))

    def __ne__(self, other):
        return not (self == other)

    @property
    def x(self):
        """int: The x position of the upper left corner of the rectangle."""
        return self._ptr.x

    @x.setter
    def x(self, value):
        self._ptr.x = value

    @property
    def y(self):
        """int: The y position of the upper left corner of the rectangle."""
        return self._ptr.y

    @y.setter
    def y(self, value):
        self._ptr.y = value

    @property
    def w(self):
        """int: The width of the rectangle."""
        return self._ptr.w

    @w.setter
    def w(self, value):
        self._ptr.w = value

    @property
    def h(self):
        """The height of the rectangle."""
        return self._ptr.h

    @h.setter
    def h(self, value):
        self._ptr.h = value

    def has_intersection(self, other):
        """Return whether this rectangle intersects with another rectangle.

        Args:
            other (Rect): The rectangle to test intersection with.

        Returns:
            bool: True if there is an intersection, False otherwise.
        """
        return bool(lib.SDL_HasIntersection(self._ptr, other._ptr))

    def intersect(self, other):
        """Calculate the intersection of this rectangle and another rectangle.

        Args:
            other (Rect): The other rectangle.

        Returns:
            Rect: The intersection of this rectangle and the given other rectangle, or None if there is no such
                intersection.
        """
        intersection = Rect()
        if lib.SDL_IntersectRect(self._ptr, self._ptr, intersection._ptr):
            return intersection
        else:
            return None

    def union(self, other):
        """Calculate the union of this rectangle and another rectangle.

        Args:
            other (Rect): The other rectangle.

        Returns:
            Rect: The union of this rectangle and the given other rectangle.
        """
        union = Rect()
        lib.SDL_UnionRect(self._ptr, other._ptr, union._ptr)
        return union
         
