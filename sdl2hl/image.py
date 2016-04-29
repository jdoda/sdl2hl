from enum import IntEnum

from sdl2._sdl2 import lib
from error import check_int_err, check_ptr_err
import enumtools

from surface import Surface
from renderer import Texture


class ImageInitFlag(IntEnum):
    jpg = lib.IMG_INIT_JPG
    png = lib.IMG_INIT_PNG
    tif = lib.IMG_INIT_TIF
    webp = lib.IMG_INIT_WEBP


def init(*flags):
    """Loads dynamic libraries and prepares them for use.

    Args:
        *flags (Set[ImageInitFlag]): The desired image file formats.
    """
    check_int_err(lib.IMG_Init(enumtools.get_mask(flags)))


def quit():
    """Indicate that we are ready to unload the dynamically loaded libraries."""
    lib.IMG_Quit()


def load(file):
    """Load an image from a file name in a new surface. Type detected from file name.
    Args
        file: The name of the image file.

    Returns:
        A new surface.

    """
    return Surface._from_ptr(check_ptr_err(lib.IMG_Load(file)))


def load_texture(renderer, file):
    """Load an image directly into a render texture.
    Args:
        renderer: The renderer to make the texture.
        file: The image file to load.

    Returns:
        A new texture
    """
    return Texture._from_ptr(check_ptr_err(lib.IMG_LoadTexture(renderer._ptr, file)))


def save(surface, file):
    """Save a png image of the surface.
    Args:
        surface: The surface to save.
        file: The file path to save to.

    """
    check_int_err(lib.IMG_SavePNG(surface._ptr, file))