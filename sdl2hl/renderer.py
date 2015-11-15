from sdl2._sdl2 import ffi, lib
from error import check_int_err, check_ptr_err
import rect


class Renderer(object):

    @staticmethod
    def _from_ptr(ptr):
        renderer = object.__new__(Renderer)
        renderer._ptr = ptr
        return renderer

    @staticmethod
    def create_software_renderer(self, surface):
        renderer = object.__new__(Renderer)
        renderer._ptr = self._ptr = check_ptr_err(lib.SDL_CreateSoftwareRenderer(surface._ptr))
        return renderer

    def __init__(self, window, index=-1, flags=0):
        self._ptr = check_ptr_err(lib.SDL_CreateRenderer(window._ptr, index, flags))

    def __del__(self):
        lib.SDL_DestroyRenderer(self._ptr)

    def _get_renderer_info(self):
        info = ffi.new('SDL_RendererInfo *')
        check_int_err(lib.SDL_GetRendererInfo(self._ptr, info))
        return info

    @property
    def name(self):
        return self._get_renderer_info().name

    @property
    def flags(self):
        return self._get_renderer_info().flags

    @property
    def texture_formats(self):
        info = self._get_renderer_info()
        return [info.texture_formats[i] for i in range(info.num_texture_formats)]

    @property
    def max_texture_width(self):
        return self._get_renderer_info().max_texture_width

    @property
    def max_texture_height(self):
        return self._get_renderer_info().max_texture_height

    @property
    def draw_color(self):
        rgba = ffi.new('Uint8[]', 4)
        check_int_err(lib.SDL_GetRenderDrawColor(self._ptr, rgba + 0, rgba + 1, rgba + 2, rgba + 3))
        return (rgba[0], rgba[1], rgba[2], rgba[3])

    @draw_color.setter
    def draw_color(self, rgba):
        r, g, b, a = rgba
        check_int_err(lib.SDL_SetRenderDrawColor(self._ptr, r, g, b, a))

    @property
    def draw_blend_mode(self):
        blend_mode = ffi.new('SDL_BlendMode *')
        check_int_err(lib.SDL_GetRenderDrawBlendMode(self._ptr, blend_mode))
        return blend_mode[0]

    @draw_blend_mode.setter
    def draw_blend_mode(self, blend_mode):
        check_int_err(lib.SDL_SetRenderDrawBlendMode(self._ptr, blend_mode))

    @property
    def viewport(self):
        viewport = rect.Rect(0, 0, 0, 0)
        check_int_err(lib.SDL_RenderGetViewport(self._ptr, viewport._ptr))
        return viewport

    @viewport.setter
    def viewport(self, viewport):
        check_int_err(lib.SDL_RenderSetViewport(self._ptr, viewport._ptr))

    @property
    def render_target_supported(self):
        return bool(lib.SDL_RenderTargetSupported(self._ptr))

    def set_render_target(self, texture):
        check_int_err(lib.SDL_SetRenderTarget(self._ptr, texture._ptr))

    def clear(self):
        check_int_err(lib.SDL_RenderClear(self._ptr))

    def draw_line(self, x1, y1, x2, y2):
        check_int_err(lib.SDL_RenderDrawLine(self._ptr, x1, y1, x2, y2))

    def draw_lines(self, points):
        point_array = ffi.new('SDL_Point[]', len(points))
        for i, p in enumerate(points):
            point_array[i] = p._ptr
        check_int_err(lib.SDL_RenderDrawLines(self._ptr, point_array, len(points)))

    def draw_point(self, x, y):
        check_int_err(lib.SDL_RenderDrawPoint(self._ptr, x, y))

    def draw_points(self, points):
        point_array = ffi.new('SDL_Point[]', len(points))
        for i, p in enumerate(points):
            point_array[i] = p._ptr
        check_int_err(lib.SDL_RenderDrawPoints(self._ptr, point_array, len(points)))

    def draw_rect(self, rect):
        check_int_err(lib.SDL_RenderDrawRect(self._ptr, rect._ptr))

    def draw_rects(self, rects):
        rect_array = ffi.new('SDL_Rect[]', len(rects))
        for i, r in enumerate(rects):
            rect_array[i] = r._ptr
        check_int_err(lib.SDL_RenderDrawRects(self._ptr, rect_array, len(rects)))

    def fill_rect(self, rect):
        check_int_err(lib.SDL_RenderFillRect(self._ptr, rect._ptr))

    def fill_rects(self, rects):
        rect_array = ffi.new('SDL_Rect[]', len(rects))
        for i, r in enumerate(rects):
            rect_array[i] = r._ptr
        check_int_err(lib.SDL_RenderFillRects(self._ptr, rect_array, len(rects)))

    def copy(self, texture, source_rect=ffi.NULL, dest_rect=ffi.NULL, rotation=0, center=ffi.NULL, flip=lib.SDL_FLIP_NONE):
        if source_rect != ffi.NULL:
            source_rect = source_rect._ptr
        if dest_rect != ffi.NULL:
            dest_rect = dest_rect._ptr
        if center != ffi.NULL:
            center = center._ptr
        check_int_err(lib.SDL_RenderCopyEx(self._ptr, texture._ptr, source_rect, dest_rect, rotation, center, flip))

    def present(self):
        lib.SDL_RenderPresent(self._ptr)


class Texture(object):

    @staticmethod
    def from_image(renderer, path):
        texture = object.__new__(Texture)
        texture._ptr = check_ptr_err(lib.IMG_LoadTexture(renderer._ptr, path))
        return texture

    @staticmethod
    def from_surface(renderer, surface):
        texture = object.__new__(Texture)
        texture._ptr = check_ptr_err(lib.SDL_CreateTextureFromSurface(renderer._ptr, surface._ptr))
        return texture

    def __init__(self, renderer, fmt, access, width, height):
        self._ptr = check_ptr_err(lib.SDL_CreateTexture(renderer._ptr, fmt, access, width, height))

    def __del__(self):
        lib.SDL_DestroyTexture(self._ptr)

    @property
    def format(self):
        fmt = ffi.new('Uint32 *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, fmt, ffi.NULL, ffi.NULL, ffi.NULL))
        return fmt[0]

    @property
    def access(self):
        access = ffi.new('int *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, ffi.NULL, access, ffi.NULL, ffi.NULL))
        return access[0]

    @property
    def width(self):
        width = ffi.new('int *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, ffi.NULL, ffi.NULL, width, ffi.NULL))
        return width[0]

    @property
    def height(self):
        height = ffi.new('int *')
        check_int_err(lib.SDL_QueryTexture(self._ptr, ffi.NULL, ffi.NULL, ffi.NULL, height))
        return height[0]

    @property
    def color_mod(self):
        rgb = ffi.new('Uint8[]', 3)
        check_int_err(lib.SDL_GetTextureColorMod(self._ptr, rgb + 0, rgb + 1, rgb + 2))
        return (rgb[0], rgb[1], rgb[2])

    @color_mod.setter
    def color_mod(self, rgb):
        r, g, b = rgb
        check_int_err(lib.SDL_SetTextureColorMod(self._ptr, r, g, b))

    @property
    def alpha_mod(self):
        a = ffi.new('Uint8 *')
        check_int_err(lib.SDL_GetTextureAlphaMod(self._ptr, a))
        return a[0]

    @alpha_mod.setter
    def alpha_mod(self, a):
        check_int_err(lib.SDL_SetTextureAlphaMod(self._ptr, a))

    @property
    def blend_mode(self):
        blend_mode = ffi.new('SDL_BlendMode *')
        check_int_err(lib.SDL_GetTextureBlendMode(self._ptr, blend_mode))
        return blend_mode[0]

    @blend_mode.setter
    def blend_mode(self, blend_mode):
        check_int_err(lib.SDL_SetTextureBlendMode(self._ptr, blend_mode))
    
