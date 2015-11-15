import weakref

from sdl2._sdl2 import ffi, lib

from error import check_int_err

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
    """Pumps the event loop, gathering events from the input devices.
    This function updates the event queue and internal input device state.
    This should only be run in the thread that sets the video mode.
    """
    lib.SDL_PumpEvents()

def peek(quantity, min_type=lib.SDL_FIRSTEVENT, max_type=lib.SDL_LASTEVENT):
    """Return events at the front of the event queue, within the specified minimum and maximum type,
    and do not remove them from the queue.

    Args:
        quantity (int): The maximum number of events to return.
        min_type (int): The minimum value for the event type of the returned events.
        max_type (int): The maximum value for the event type of the returned events.

    Returns:
        List[Event]: Events from the front of the event queue.

    Raises:
        SDLError: If there was an error retrieving the events.
    """

    return _peep(quantity, lib.SDL_PEEKEVENT, min_type, max_type)

def get(quantity, min_type=lib.SDL_FIRSTEVENT, max_type=lib.SDL_LASTEVENT):
    """Return events at the front of the event queue, within the specified minimum and maximum type,
    and remove them from the queue.

    Args:
        quantity (int): The maximum number of events to return.
        min_type (int): The minimum value for the event type of the returned events.
        max_type (int): The maximum value for the event type of the returned events.

    Returns:
        List[Event]: Events from the front of the event queue.

    Raises:
        SDLError: If there was an error retrieving the events.
    """
    return _peep(quantity, lib.SDL_GETEVENT, min_type, max_type)

def _peep(quantity, action, min_type, max_type):
    events = ffi.new('SDL_Event[]', quantity)
    quantity_retrieved = check_int_err(lib.SDL_PeepEvents(events, quantity, action, min_type, max_type))

    result = []
    for i in range(quantity_retrieved):
        event_ptr = events + i
        _event_reference_map[event_ptr] = events
        result.append(Event._from_ptr(event_ptr))
    return result

def poll():
    """Polls for currently pending events.

    Returns:
        Iterable[Event]: Events from the event queue.
    """
    event = Event()
    while lib.SDL_PollEvent(event._ptr):
        yield event
        event = Event()
    
