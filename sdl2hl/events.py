from enum import IntEnum
import weakref

from sdl2._sdl2 import ffi, lib

from error import check_int_err
from keycode import KeyCode, KeyMod
from scancode import ScanCode
from enumtools import get_items
from gamecontroller import ControllerAxis, ControllerButton


_event_reference_map = weakref.WeakKeyDictionary()
_event_userdata = set()


class EventType(IntEnum):
    firstevent = lib.SDL_FIRSTEVENT

    quit = lib.SDL_QUIT #: User-requested quit

    # Window events
    windowevent = lib.SDL_WINDOWEVENT #: Window state change
    syswmevent = lib.SDL_SYSWMEVENT #: System specific event

    # Keyboard events
    keydown = lib.SDL_KEYDOWN #: Key pressed
    keyup = lib.SDL_KEYUP #: Key released
    textediting = lib.SDL_TEXTEDITING #: Keyboard text editing (composition)
    textinput = lib.SDL_TEXTINPUT #: Keyboard text input
    keymapchanged = lib.SDL_KEYMAPCHANGED #: Keymap changed due to a system event such as an input language or keyboard layout change.

    # Mouse events
    mousemotion = lib.SDL_MOUSEMOTION #: Mouse moved
    mousebuttondown = lib.SDL_MOUSEBUTTONDOWN #: Mouse button pressed
    mousebuttonup = lib.SDL_MOUSEBUTTONUP #: Mouse button released
    mousewheel = lib.SDL_MOUSEWHEEL #: Mouse wheel motion

    # Joystick events
    joyaxismotion = lib.SDL_JOYAXISMOTION #: Joystick axis motion
    joyballmotion = lib.SDL_JOYBALLMOTION #: Joystick trackball motion
    joyhatmotion = lib.SDL_JOYHATMOTION #: Joystick hat position change
    joybuttondown = lib.SDL_JOYBUTTONDOWN #: Joystick button pressed
    joybuttonup = lib.SDL_JOYBUTTONUP #: Joystick button released
    joydeviceadded = lib.SDL_JOYDEVICEADDED #: A new joystick has been inserted into the system
    joydeviceremoved = lib.SDL_JOYDEVICEREMOVED #: An opened joystick has been removed

    # Game controller events
    controlleraxismotion = lib.SDL_CONTROLLERAXISMOTION #: Game controller axis motion
    controllerbuttondown = lib.SDL_CONTROLLERBUTTONDOWN #: Game controller button pressed
    controllerbuttonup = lib.SDL_CONTROLLERBUTTONUP #: Game controller button released
    controllerdeviceadded = lib.SDL_CONTROLLERDEVICEADDED #: A new Game controller has been inserted into the system
    controllerdeviceremoved = lib.SDL_CONTROLLERDEVICEREMOVED #: An opened Game controller has been removed
    controllerdeviceremapped = lib.SDL_CONTROLLERDEVICEREMAPPED #: The controller mapping was updated

    # Touch events
    fingerdown = lib.SDL_FINGERDOWN
    fingerup = lib.SDL_FINGERUP
    fingermotion = lib.SDL_FINGERMOTION

    # Gesture events
    dollargesture = lib.SDL_DOLLARGESTURE
    dollarrecord = lib.SDL_DOLLARRECORD
    multigesture = lib.SDL_MULTIGESTURE

    # Clipboard events
    clipboardupdate = lib.SDL_CLIPBOARDUPDATE #: The clipboard changed

    # Drag and drop events
    dropfile = lib.SDL_DROPFILE #: The system requests a file open

    # Audio hotplug events
    audiodeviceadded = lib.SDL_AUDIODEVICEADDED #: A new audio device is available
    audiodeviceremoved = lib.SDL_AUDIODEVICEREMOVED #: An audio device has been removed.

    # Render events
    render_targets_reset = lib.SDL_RENDER_TARGETS_RESET #: The render targets have been reset and their contents need to be updated
    render_device_reset = lib.SDL_RENDER_DEVICE_RESET #: The device has been reset and all textures need to be recreated
    
    lastevent = lib.SDL_LASTEVENT


class WindowEventType(IntEnum):
    close = lib.SDL_WINDOWEVENT_CLOSE
    enter = lib.SDL_WINDOWEVENT_ENTER
    exposed = lib.SDL_WINDOWEVENT_EXPOSED
    focus_gained = lib.SDL_WINDOWEVENT_FOCUS_GAINED
    focus_lost = lib.SDL_WINDOWEVENT_FOCUS_LOST
    hidden = lib.SDL_WINDOWEVENT_HIDDEN
    leave = lib.SDL_WINDOWEVENT_LEAVE
    maximized = lib.SDL_WINDOWEVENT_MAXIMIZED
    minimized = lib.SDL_WINDOWEVENT_MINIMIZED
    moved = lib.SDL_WINDOWEVENT_MOVED
    none = lib.SDL_WINDOWEVENT_NONE
    resized = lib.SDL_WINDOWEVENT_RESIZED
    restored = lib.SDL_WINDOWEVENT_RESTORED
    shown = lib.SDL_WINDOWEVENT_SHOWN
    size_changed = lib.SDL_WINDOWEVENT_SIZE_CHANGED


class KeyState(IntEnum):
    pressed = lib.SDL_PRESSED
    released = lib.SDL_RELEASED


class Event(object):

    @staticmethod
    def _from_ptr(ptr):
        event_class = _EVENT_TYPES.get(ptr.type, Event)
        event = object.__new__(event_class)
        event._ptr = ptr
        return event

    def __init__(self):
        self._ptr = ffi.new('SDL_Event *')

    @property
    def type(self):
        """EventType: The type of the event."""
        return EventType(self._ptr.common.type)

    @property
    def timestamp(self):
        """int: The timestamp of the event."""
        return self._ptr.common.timestamp


class QuitEvent(Event):
    pass
    

class WindowEvent(Event):

    @property
    def window_id(self):
        """int: The id of the associated window."""
        return self._ptr.window.windowID

    @property
    def event(self):
        """WindowEventType: The type of window event."""
        return WindowEventType(self._ptr.window.event)


class KeyboardEvent(Event):

    @property
    def window_id(self):
        """int: The id of window with keyboard focus, if any."""
        return self._ptr.key.windowID

    @property
    def state(self):
        """KeyState: The state of the key."""
        return KeyState(self._ptr.key.state)

    @property
    def repeat(self):
        """bool: True if this is a key repeat."""
        return bool(self._ptr.key.repeat)

    @property
    def scancode(self):
        """ScanCode: Physical keycode."""
        return ScanCode(self._ptr.key.keysym.scancode)

    @property
    def keycode(self):
        """KeyCode: Virtual keycode."""
        return KeyCode(self._ptr.key.keysym.sym)

    @property
    def mod(self):
        """Set[KeyMod]: The current key modifiers."""
        return get_items(KeyMod, self._ptr.key.keysym.mod)


class TextInputEvent(Event):
    
    @property
    def window_id(self):
        """int: The id of the window with keyboard focus, if any."""
        return self._ptr.text.windowID
        
    @property
    def text(self):
        """str: The input text."""
        return ffi.string(self._ptr.text.text)
        
        
class MouseMotionEvent(Event):

    @property
    def window_id(self):
        """int: The id of the associated window."""
        return self._ptr.motion.windowID
        
    @property
    def which(self):
        """int: The id of the mouse that generated the event."""
        return self._ptr.motion.which
        
    @property
    def state(self):
        """int: The current button state."""
        return self._ptr.motion.state
    
    @property
    def x(self):
        """int: The x coordinate, relative to the windows."""
        return self._ptr.motion.x
        
    @property
    def x(self):
        """int: The x coordinate, relative to the window."""
        return self._ptr.motion.x
        
    @property
    def y(self):
        """int: The y coordinate, relative to the window."""
        return self._ptr.motion.y
    
    @property
    def xrel(self):
        """int: The relative motion in the x direction."""
        return self._ptr.motion.xrel
        
    @property
    def yrel(self):
        """int: The relative motion in the y direction."""
        return self._ptr.motion.yrel


class MouseButtonEvent(Event):

    @property
    def window_id(self):
        """int: The id of the associated window."""
        return self._ptr.button.windowID
        
    @property
    def which(self):
        """int: The id of the mouse that generated the event."""
        return self._ptr.button.which
        
    @property
    def button(self):
        """int: The mouse button index."""
        return self._ptr.button.button

    @property
    def state(self):
        """KeyState: The state of the mouse button."""
        return KeyState(self._ptr.button.state)
        
    @property
    def clicks(self):
        """int: The number of clicks (single, double, etc.)."""
        return self._ptr.button.clicks
        
    @property
    def x(self):
        """int: The x coordinate, relative to the window."""
        return self._ptr.button.x
        
    @property
    def y(self):
        """int: The y coordinate, relative to the window."""
        return self._ptr.button.y


class ControllerAxisEvent(Event):
    
    @property
    def which(self):
        """int: The controller instance id."""
        return self._ptr.caxis.which
    
    @property
    def axis(self):
        """ControllerAxis: The controller axis."""
        return ControllerAxis(self._ptr.caxis.axis)

    @property
    def value(self):
        """int: The axis value (range: -32768 to 32767)."""
        return self._ptr.caxis.value


class ControllerButtonEvent(Event):
    
    @property
    def which(self):
        """int: The controller instance id."""
        return self._ptr.cbutton.which
        
    @property
    def button(self):
        """ControllerButton: The controller button."""
        return ControllerButton(self._ptr.cbutton.button)
        
    @property
    def state(self):
        """KeyState: The button state."""
        return KeyState(self._ptr.cbutton.state)


def pump():
    """Pumps the event loop, gathering events from the input devices.
    This function updates the event queue and internal input device state.
    This should only be run in the thread that sets the video mode.
    """
    lib.SDL_PumpEvents()

def peek(quantity, min_type=EventType.firstevent, max_type=EventType.lastevent):
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

def get(quantity, min_type=EventType.firstevent, max_type=EventType.lastevent):
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
    event_ptr = ffi.new('SDL_Event *')
    while lib.SDL_PollEvent(event_ptr):
        yield Event._from_ptr(event_ptr)
        event = ffi.new('SDL_Event *')
      
        
_EVENT_TYPES = {
    EventType.quit : QuitEvent,
    EventType.windowevent: WindowEvent,
    EventType.keydown : KeyboardEvent,
    EventType.keyup : KeyboardEvent,
    EventType.textinput : TextInputEvent,
    EventType.mousemotion : MouseMotionEvent,
    EventType.mousebuttondown : MouseButtonEvent,
    EventType.mousebuttonup : MouseButtonEvent,
    EventType.controlleraxismotion : ControllerAxisEvent,
    EventType.controllerbuttondown : ControllerButtonEvent,
    EventType.controllerbuttonup : ControllerButtonEvent,
}
    
