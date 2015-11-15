import weakref

from sdl2._sdl2 import ffi, lib


_event_reference_map = weakref.WeakKeyDictionary()


class Event(object):

    types = {lib.SDL_KEYDOWN : 'key',
             lib.SDL_KEYUP : 'key',
             lib.SDL_JOYAXISMOTION : 'jaxis',
             lib.SDL_JOYBALLMOTION : 'jball',
             lib.SDL_JOYHATMOTION : 'jhat',
             lib.SDL_JOYBUTTONDOWN : 'jbutton',
             lib.SDL_JOYBUTTONUP : 'jbutton',
             lib.SDL_MOUSEMOTION : 'motion',
             lib.SDL_MOUSEBUTTONDOWN : 'button',
             lib.SDL_MOUSEBUTTONUP : 'button',
             lib.SDL_MOUSEWHEEL : 'wheel',
             lib.SDL_QUIT : 'quit',
             lib.SDL_SYSWMEVENT : 'syswm',
             lib.SDL_TEXTEDITING : 'edit',
             lib.SDL_TEXTINPUT : 'text',
             lib.SDL_USEREVENT : 'user',
             lib.SDL_WINDOWEVENT : 'window'}

    @staticmethod
    def _from_ptr(ptr):
        event = object.__new__(Event)
        event._ptr = ptr
        return event

    def __init__(self):
        self._ptr = ffi.new('SDL_Event *')

    @property
    def type(self):
        return self._ptr.type

    def __getattr__(self, name):
        return getattr(getattr(self._ptr, Event.types[self._ptr.type]), name)


def pump():
    lib.SDL_PumpEvents()

def peek(quantity, min_type=lib.SDL_FIRSTEVENT, max_type=lib.SDL_LASTEVENT):
    events = ffi.new('SDL_Event[]', quantity)
    quantity_retrieved = lib.SDL_PeepEvents(events, quantity, lib.SDL_PEEKEVENT, min_type, max_type)

    result = []
    for i in range(quantity_retrieved):
        event_ptr = events + i
        _event_reference_map[event_ptr] = events
        result.append(Event._from_ptr(event_ptr))
    return result

def get(quantity, min_type=lib.SDL_FIRSTEVENT, max_type=lib.SDL_LASTEVENT):
    events = ffi.new('SDL_Event[]', quantity)
    quantity_retrieved = lib.SDL_PeepEvents(events, quantity, lib.SDL_GETEVENT, min_type, max_type)

    result = []
    for i in range(quantity_retrieved):
        event_ptr = events + i
        _event_reference_map[event_ptr] = events
        result.append(Event._from_ptr(event_ptr))
    return result

def poll():
    event = Event()
    while lib.SDL_PollEvent(event._ptr):
        yield event
        event = Event()
    
