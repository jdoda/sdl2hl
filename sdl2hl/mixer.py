from enum import IntEnum

from sdl2._sdl2 import lib
from error import check_int_err, check_ptr_err
import enumtools


class AudioInitFlag(IntEnum):
    flac = lib.MIX_INIT_FLAC
    mod = lib.MIX_INIT_MOD
    mp3 = lib.MIX_INIT_MP3
    ogg = lib.MIX_INIT_OGG
    
    
class AudioFormat(IntEnum):
    u8 = lib.AUDIO_U8 #: Unsigned 8-bit samples
    s8 = lib.AUDIO_S8 #: Signed 8-bit samples
    u16lsb = lib.AUDIO_U16LSB #: Unsigned 16-bit samples, in little-endian byte order
    s16lsb = lib.AUDIO_S16LSB #: Signed 16-bit samples, in little-endian byte order
    u16msb = lib.AUDIO_U16MSB #: Unsigned 16-bit samples, in big-endian byte order
    s16msb = lib.AUDIO_S16MSB #: Signed 16-bit samples, in big-endian byte order
    u16sys = lib.AUDIO_U16SYS #: Unsigned 16-bit samples, in system byte order
    s16sys = lib.AUDIO_S16SYS #: Signed 16-bit samples, in system byte order
    default = lib.AUDIO_S16SYS


class Chunk(object):

    @staticmethod
    def from_path(path):
        rw = check_ptr_err(lib.SDL_RWFromFile(path, "rb"))
        chunk = object.__new__(Chunk)
        chunk._ptr = check_ptr_err(lib.Mix_LoadWAV_RW(rw, 1))
        return chunk
    
    def __init__(self, audio_bytes):
        rw = check_ptr_err(lib.SDL_RWFromConstMem(audio_bytes, len(audio_bytes)))
        self._ptr = check_ptr_err(lib.Mix_LoadWAV_RW(rw, 1))
        
    def __del__(self):
        lib.Mix_FreeChunk(self._ptr)
    
    @property    
    def volume(self):
        return lib.Mix_VolumeChunk(self._ptr, -1)
        
    @volume.setter
    def volume(self, volume):
        lib.Mix_VolumeChunk(self._ptr, volume) 
        
    def play(self, loops=0, duration=-1):
        channel_index = check_int_err(lib.Mix_PlayChannelTimed(-1, self._ptr, loops, duration))
        return Channel(channel_index)
        
    def fade_in(self, fade_duration, loops=0, duration=-1):
        channel_index = check_int_err(lib.Mix_FadeInChannelTimed(-1, self._ptr, loops, fade_duration, duration))
        return Channel(channel_index)
        

class Channel(object):

    def __init__(self, index):
        self._index = index
        
    @property
    def index(self):
        return self._index
        
    @property
    def volume(self):
        return lib.Mix_Volume(self._index, -1)
    
    @volume.setter
    def volume(self, volume):
        lib.Mix_Volume(self._index, volume)
        
    def pause(self):
        lib.Mix_Pause(self._index)
        
    def resume(self):
        lib.Mix_Resume(self._index)
    
    def halt(self):
        lib.Mix_HaltChannel(self._index)
        

ALL_CHANNELS = Channel(-1)

def init(*flags):
    """Loads dynamic libraries and prepares them for use.
    
    Args:
        *flags (Set[AudioInitFlag]): The desired audio file formats.
    """
    lib.Mix_Init(enumtools.get_mask(flags))
    
def quit():
    """Indicate that we are ready to unload the dynamically loaded libraries."""
    lib.Mix_Quit()
    
def open_audio(frequency=44100, format=AudioFormat.default, channels=2, chunksize=1024):
    """Open the mixer with a certain audio format.
    
    Args:
        frequency (int): Output sampling frequency in samples per second (Hz).
        format (AudioFormat): Output sample format.
        channels (int): Number of sound channels in output. Set to 2 for stereo, 1 for mono.
        chunksize (int): Bytes used per output sample.
        
    Raises:
        SDLError: If the audio device cannot be opened.
    """
    check_int_err(lib.Mix_OpenAudio(frequency, format, channels, chunksize))

def close_audio():
    """Close the mixer, halting all playing audio."""
    lib.Mix_CloseAudio()
    
def allocate_channels(count):
    """Set the number of channels to mix.
    
    Args:
        count (int): The number of channels to mix.
        
    Returns:
        int: The number of channels being mixed.
    """
    return lib.Mix_AllocateChannels(count)
    
