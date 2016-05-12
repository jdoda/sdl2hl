from enum import IntEnum

from sdl2._sdl2 import ffi, lib
from error import check_int_err, check_ptr_err
import enumtools


class WindowFlags(IntEnum):
    allow_highdpi = lib.SDL_WINDOW_ALLOW_HIGHDPI
    borderless = lib.SDL_WINDOW_BORDERLESS
    foreign = lib.SDL_WINDOW_FOREIGN
    fullscreen = lib.SDL_WINDOW_FULLSCREEN
    fullscreen_desktop = lib.SDL_WINDOW_FULLSCREEN_DESKTOP
    hidden = lib.SDL_WINDOW_HIDDEN
    input_focus = lib.SDL_WINDOW_INPUT_FOCUS
    input_grabbed = lib.SDL_WINDOW_INPUT_GRABBED
    maximized = lib.SDL_WINDOW_MAXIMIZED
    minimized = lib.SDL_WINDOW_MINIMIZED
    mouse_focus = lib.SDL_WINDOW_MOUSE_FOCUS
    opengl = lib.SDL_WINDOW_OPENGL
    resizable = lib.SDL_WINDOW_RESIZABLE
    shown = lib.SDL_WINDOW_SHOWN


class Window(object):
    """The type used to identify a window."""

    def __init__(self, title='sdl2', x=lib.SDL_WINDOWPOS_CENTERED, y=lib.SDL_WINDOWPOS_CENTERED,
                 w=640, h=480, flags=frozenset()):
        """Create a window with the specified position, dimensions, and flags.

        Args:
            title (str): The title of the window.
            x (int): The x postion of the window.
            y (int): The y position of the window.
            w (int): The width of the window.
            h (int): The height of the window.
            flags (Set[WindowFlags]): The flags for the window.
        Raises:
            SDLError: If the window could not be created.
        """
        self._ptr = check_ptr_err(lib.SDL_CreateWindow(title.encode('utf-8'), x, y, w, h, enumtools.get_mask(flags)))

    def __del__(self):
        lib.SDL_DestroyWindow(self._ptr)

    @property
    def flags(self):
        """set[WindowFlags]: The flags for the window."""
        return enumtools.get_items(WindowFlags, lib.SDL_GetWindowFlags(self._ptr))

    @property
    def title(self):
        """str: The title of the window."""
        return ffi.string(lib.SDL_GetWindowTitle(self._ptr))

    @title.setter
    def title(self, title):
        lib.SDL_SetWindowTitle(self._ptr, title.encode('utf-8'))

    @property
    def position(self):
        """Tuple[int, int]: The x and y position of the window."""
        position = ffi.new('int[]', 2)
        lib.SDL_GetWindowPosition(self._ptr, position + 0, position + 1)
        return (position[0], position[1])

    @position.setter
    def position(self, position):
        x, y = position
        lib.SDL_SetWindowPosition(self._ptr, x, y)

    @property
    def size(self):
        """Tuple[int, int]: The width and height of the window."""
        size = ffi.new('int[]', 2)
        lib.SDL_GetWindowSize(self._ptr, size + 0, size + 1)
        return (size[0], size[1])

    @size.setter
    def size(self, size):
        w, h = size
        lib.SDL_SetWindowSize(self._ptr, w, h)

    def show(self):
        """Show the window."""
        lib.SDL_ShowWindow(self._ptr)

    def hide(self):
        """Hide the window."""
        lib.SDL_HideWindow(self._ptr)

    def raise_(self):
        """Raise the window above other windows and set the input focus."""
        lib.SDL_RaiseWindow(self._ptr)

    def maximize(self):
        """Make the window as large as possible."""
        lib.SDL_MaximizeWindow(self._ptr)

    def minimize(self):
        """Minimize the window to an iconic representation."""
        lib.SDL_MinimizeWindow(self._ptr)

    def restore(self):
        """Restore the size and position of a minimized or maximized window."""
        lib.SDL_RestoreWindow(self._ptr)

    def set_fullscreen(self, flag):
        check_int_err(lib.SDL_SetWindowFullscreen(self._ptr, flag))

    def swap(self):
        """Swap the OpenGL buffers, if double-buffering is supported."""
        lib.SDL_GL_SwapWindow(self._ptr)


class GLContext(object):
    """A handle to an OpenGL context."""

    def __init__(self, window):
        """Create an OpenGL context for use with an OpenGL window, and make it current.

        Args:
            window (Window): The window that this OpenGL context will be used with.
        """
        self._ptr = lib.SDL_GL_CreateContext(window._ptr)

    def __del__(self):
        lib.SDL_GL_DeleteContext(self._ptr)
    


class Display(object):
    """The type used to identify a display"""


    def __init__(self, index):
        """Create a new Display for the given index"""
        self._index = index

    def get_desktop_size(self):
        """Get the size of the desktop display"""

        _ptr = ffi.new('SDL_DisplayMode *')
        check_int_err(lib.SDL_GetDesktopDisplayMode(self._index, _ptr))
        return (_ptr.w, _ptr.h)
