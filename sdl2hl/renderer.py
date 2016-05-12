from enum import IntEnum

from sdl2._sdl2 import ffi, lib
from error import check_int_err, check_ptr_err
from pixels import PixelFormat
import rect
import enumtools


class RendererFlags(IntEnum):
    """Flags used when creating a rendering context."""
    software = lib.SDL_RENDERER_SOFTWARE #: The renderer is a software fallback.
    accelerated = lib.SDL_RENDERER_ACCELERATED #: The renderer uses hardware acceleration.
    presentvsync = lib.SDL_RENDERER_PRESENTVSYNC #: Present is synchronized with the refresh rate.
    targettexture = lib.SDL_RENDERER_TARGETTEXTURE #: The renderer supports rendering to texture.


class BlendMode(IntEnum):
    add = lib.SDL_BLENDMODE_ADD
    blend = lib.SDL_BLENDMODE_BLEND
    mod = lib.SDL_BLENDMODE_MOD
    none = lib.SDL_BLENDMODE_NONE


class Renderer(object):

    @staticmethod
    def _from_ptr(ptr):
        renderer = object.__new__(Renderer)
        renderer._ptr = ptr
        return renderer

    @staticmethod
    def create_software_renderer(self, surface):
        """Create a 2D software rendering context for a surface.

        Args:
            surface (Surface): The surface where rendering is done.

        Returns:
            Renderer: A 2D software rendering context.

        Raises:
            SDLError: If there was an error creating the renderer.
        """
        renderer = object.__new__(Renderer)
        renderer._ptr = self._ptr = check_ptr_err(lib.SDL_CreateSoftwareRenderer(surface._ptr))
        return renderer

    def __init__(self, window, index=-1, flags=frozenset()):
        """Create a 2D rendering context for a window.

        Args:
            window (Window): The window where rendering is displayed.
            index (int): The index of the rendering driver to initialize, or -1 to initialize the first one supporting
                         the requested flags.
            flags (Set[RendererFlags]): The requested renderer flags.

        Raises:
            SDLError: If there was an error creating the renderer.
        """
        self._ptr = check_ptr_err(lib.SDL_CreateRenderer(window._ptr, index, enumtools.get_mask(flags)))

    def __del__(self):
        lib.SDL_DestroyRenderer(self._ptr)

    def _get_renderer_info(self):
        info = ffi.new('SDL_RendererInfo *')
        check_int_err(lib.SDL_GetRendererInfo(self._ptr, info))
        return info

    @property
    def name(self):
        """str: The name of the renderer."""
        return self._get_renderer_info().name

    @property
    def flags(self):
        """Set[RendererFlags]: Supported renderer flags."""
        return enumtools.get_items(RendererFlags, self._get_renderer_info().flags)

    @property
    def texture_formats(self):
        """Set[PixelFormat]: The available texture formats."""
        info = self._get_renderer_info()
        return {PixelFormat(info.texture_formats[i]) for i in range(info.num_texture_formats)}

    @property
    def max_texture_width(self):
        """int: The maximum texture width."""
        return self._get_renderer_info().max_texture_width

    @property
    def max_texture_height(self):
        """int: The maximum texture height."""
        return self._get_renderer_info().max_texture_height

    @property
    def draw_color(self):
        """Tuple[int, int, int, int]: The color used for drawing operations in (red, green, blue, alpha) format."""
        rgba = ffi.new('Uint8[]', 4)
        check_int_err(lib.SDL_GetRenderDrawColor(self._ptr, rgba + 0, rgba + 1, rgba + 2, rgba + 3))
        return (rgba[0], rgba[1], rgba[2], rgba[3])

    @draw_color.setter
    def draw_color(self, rgba):
        r, g, b, a = rgba
        check_int_err(lib.SDL_SetRenderDrawColor(self._ptr, r, g, b, a))

    @property
    def viewport(self):
        """Rect: The drawing area for rendering on the current target."""
        viewport = rect.Rect(0, 0, 0, 0)
        check_int_err(lib.SDL_RenderGetViewport(self._ptr, viewport._ptr))
        return viewport

    @viewport.setter
    def viewport(self, viewport):
        check_int_err(lib.SDL_RenderSetViewport(self._ptr, viewport._ptr))

    @property
    def render_target_supported(self):
        """bool: Whether a window supports the use of render targets."""
        return bool(lib.SDL_RenderTargetSupported(self._ptr))

    @property
    def render_target(self):
        """Texture: The current render target, or None if using the default render target."""
        render_target = lib.SDL_GetRenderTarget(self._ptr)
        if render_target == ffi.NULL:
            return None
        else:
            return Texture._from_ptr(render_target)

    @render_target.setter
    def render_target(self, texture):
        if texture is not None:
            p = texture._ptr
        else:
            p = ffi.NULL
        check_int_err(lib.SDL_SetRenderTarget(self._ptr, p))

    @property
    def blend_mode(self):
        """BlendMode: The blend mode used for drawing operations."""
        blend_mode_ptr = ffi.new('int *')
        check_int_err(lib.SDL_GetRenderDrawBlendMode(self._ptr, blend_mode_ptr))
        return BlendMode(blend_mode_ptr[0])

    @blend_mode.setter
    def blend_mode(self, blend_mode):
        check_int_err(lib.SDL_SetRenderDrawBlendMode(self._ptr, blend_mode))

    def clear(self):
        """Clear the current rendering target with the drawing color.

         This function clears the entire rendering target, ignoring the viewport.

         Raises:
            SDLError: If an error is encountered.
         """
        check_int_err(lib.SDL_RenderClear(self._ptr))

    def draw_line(self, x1, y1, x2, y2):
        """Draw a line on the current rendering target.

        Args:
            x1 (int): The x coordinate of the start point.
            y1 (int): The y coordinate of the start point.
            x2 (int): The x coordinate of the end point.
            y2 (int): The y coordinate of the end point.

        Raises:
            SDLError: If an error is encountered.
        """
        check_int_err(lib.SDL_RenderDrawLine(self._ptr, x1, y1, x2, y2))

    def draw_lines(self, *points):
        """Draw a series of connected lines on the current rendering target.

        Args:
            *points (Point): The points along the lines.

        Raises:
            SDLError: If an error is encountered.
        """
        point_array = ffi.new('SDL_Point[]', len(points))
        for i, p in enumerate(points):
            point_array[i] = p._ptr[0]
        check_int_err(lib.SDL_RenderDrawLines(self._ptr, point_array, len(points)))

    def draw_point(self, x, y):
        """Draw a point on the current rendering target.

        Args:
            x (int): The x coordinate of the point.
            y (int): The y coordinate of the point.

        Raises:
            SDLError: If an error is encountered.
        """
        check_int_err(lib.SDL_RenderDrawPoint(self._ptr, x, y))

    def draw_points(self, *points):
        """Draw multiple points on the current rendering target.

        Args:
            *points (Point): The points to draw.

        Raises:
            SDLError: If an error is encountered.
        """
        point_array = ffi.new('SDL_Point[]', len(points))
        for i, p in enumerate(points):
            point_array[i] = p._ptr[0]
        check_int_err(lib.SDL_RenderDrawPoints(self._ptr, point_array, len(points)))

    def draw_rect(self, rect):
        """Draw a rectangle on the current rendering target.

        Args:
            rect (Rect): The destination rectangle, or None to outline the entire rendering target.

        Raises:
            SDLError: If an error is encountered.
        """
        check_int_err(lib.SDL_RenderDrawRect(self._ptr, rect._ptr))

    def draw_rects(self, *rects):
        """Draw some number of rectangles on the current rendering target.

        Args:
            *rects (Rect): The destination rectangles.

        Raises:
            SDLError: If an error is encountered.
        """
        rect_array = ffi.new('SDL_Rect[]', len(rects))
        for i, r in enumerate(rects):
            rect_array[i] = r._ptr[0]
        check_int_err(lib.SDL_RenderDrawRects(self._ptr, rect_array, len(rects)))

    def fill_rect(self, rect):
        """Fill a rectangle on the current rendering target with the drawing color.

        Args:
            rect (Rect): The destination rectangle, or None to fill the entire rendering target.

        Raises:
            SDLError: If an error is encountered.
        """
        check_int_err(lib.SDL_RenderFillRect(self._ptr, rect._ptr))

    def fill_rects(self, *rects):
        """Fill some number of rectangles on the current rendering target with the drawing color.

        Args:
            *rects (Rect): The destination rectangles.

        Raises:
            SDLError: If an error is encountered.
        """
        rect_array = ffi.new('SDL_Rect[]', len(rects))
        for i, r in enumerate(rects):
            rect_array[i] = r._ptr[0]
        check_int_err(lib.SDL_RenderFillRects(self._ptr, rect_array, len(rects)))

    def copy(self, texture, source_rect=None, dest_rect=None, rotation=0, center=None, flip=lib.SDL_FLIP_NONE):
        """Copy a portion of the source texture to the current rendering target, rotating it by angle around the given center.

        Args:
            texture (Texture): The source texture.
            source_rect (Rect): The source rectangle, or None for the entire texture.
            dest_rect (Rect): The destination rectangle, or None for the entire rendering target.
            rotation (float): An angle in degrees that indicates the rotation that will be applied to dest_rect.
            center (Point): The point around which dest_rect will be rotated (if None, rotation will be done around
                            dest_rect.w/2, dest_rect.h/2).
            flip (int): A value stating which flipping actions should be performed on the texture.

        Raises:
            SDLError: If an error is encountered.
        """
        if source_rect == None:
            source_rect_ptr = ffi.NULL
        else:
            source_rect_ptr = source_rect._ptr
            
        if dest_rect == None:
            dest_rect_ptr = ffi.NULL
        else:
            dest_rect_ptr = dest_rect._ptr

        if center == None:
            center_ptr = ffi.NULL
        else:
            center_ptr = center._ptr
            
        check_int_err(lib.SDL_RenderCopyEx(self._ptr, texture._ptr, source_rect_ptr, dest_rect_ptr, rotation, center_ptr, flip))

    def present(self):
        """Update the screen with rendering performed."""
        lib.SDL_RenderPresent(self._ptr)


class TextureAccess(IntEnum):
    static = lib.SDL_TEXTUREACCESS_STATIC #: Changes rarely, not lockable.
    streaming = lib.SDL_TEXTUREACCESS_STREAMING #: Changes frequently, lockable.
    target = lib.SDL_TEXTUREACCESS_TARGET #: Texture can be used as a render target.


class Texture(object):

    @staticmethod
    def _from_ptr(ptr):
        renderer = object.__new__(Texture)
        renderer._ptr = ptr
        return renderer

    @staticmethod
    def from_surface(renderer, surface):
        """Create a texture from an existing surface.

        Args:
            surface (Surface): The surface containing pixel data used to fill the texture.

        Returns:
            Texture: A texture containing the pixels from surface.

        Raises:
            SDLError: If an error is encountered.
        """
        texture = object.__new__(Texture)
        texture._ptr = check_ptr_err(lib.SDL_CreateTextureFromSurface(renderer._ptr, surface._ptr))
        return texture

    def __init__(self, renderer, fmt, access, w, h):
        """Create a texture for a rendering context.

        Args:
            renderer (Renderer): The renderer.
            fmt (PixelFormat): The format of the texture.
            access (TextureAccess): The access value for the texture.
            w (int): The width of the texture in pixels.
            h (int): The height of the texture in pixels.

        Raises:
            SDLError: If no rendering context was active, the format was unsupported, or the width or height were out
                      of range.
        """
        self._ptr = check_ptr_err(lib.SDL_CreateTexture(renderer._ptr, fmt, access, w, h))

    def __del__(self):
        lib.SDL_DestroyTexture(self._ptr)

    @property
    def format(self):
        """PixelFormat: The raw format of the texture. The actual format may differ, but pixel transfers will use this
                        format.
        """
        fmt = ffi.new('Uint32 *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, fmt, ffi.NULL, ffi.NULL, ffi.NULL))
        return PixelFormat(fmt[0])

    @property
    def access(self):
        """TextureAccess: The actual access to the texture."""
        access = ffi.new('int *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, ffi.NULL, access, ffi.NULL, ffi.NULL))
        return TextureAccess(access[0])

    @property
    def w(self):
        """int: The width of the texture in pixels."""
        w = ffi.new('int *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, ffi.NULL, ffi.NULL, w, ffi.NULL))
        return w[0]

    @property
    def h(self):
        """int: The height of the texture in pixels."""
        h = ffi.new('int *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, ffi.NULL, ffi.NULL, ffi.NULL, h))
        return h[0]

    @property
    def color_mod(self):
        """Tuple[int, int, int]: The additional color value used in render copy operations in (red, green, blue)
                                 format.
        """
        rgb = ffi.new('Uint8[]', 3)
        check_int_err(lib.SDL_GetTextureColorMod(self._ptr, rgb + 0, rgb + 1, rgb + 2))
        return (rgb[0], rgb[1], rgb[2])

    @color_mod.setter
    def color_mod(self, rgb):
        r, g, b = rgb
        check_int_err(lib.SDL_SetTextureColorMod(self._ptr, r, g, b))

    @property
    def alpha_mod(self):
        """int: The additional alpha value used in render copy operations."""
        a = ffi.new('Uint8 *')
        check_int_err(lib.SDL_GetTextureAlphaMod(self._ptr, a))
        return a[0]

    @alpha_mod.setter
    def alpha_mod(self, a):
        check_int_err(lib.SDL_SetTextureAlphaMod(self._ptr, a))

    @property
    def blend_mode(self):
        """BlendMode: The blend mode used for drawing operations."""
        blend_mode_ptr = ffi.new('int *')
        lib.SDL_GetTextureBlendMode(self._ptr, blend_mode_ptr)
        return BlendMode(blend_mode_ptr[0])

    @blend_mode.setter
    def blend_mode(self, blend_mode):
        check_int_err(lib.SDL_SetTextureBlendMode(self._ptr, blend_mode))
    
