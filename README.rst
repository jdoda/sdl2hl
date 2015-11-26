
sdl2hl
======

sdl2hl is a Python package providing a friendly, Pythonic wrapper around the
SDL2 library. sdl2hl calls SDL2 using Kevin Howell's sdl2-cffi package (which
can be found here: https://github.com/kahowell/sdl2-cffi). sdl2hl maintains
sdl2-cffi's advantages of using cffi and being zlib licensed, while providing
an API that hides the gruesome details of the FFI layer from the user.

Goals
-----

The goals of sdl2hl are:

- Provide a straightforward, Pythonic API on top of the functionality provided
  by SDL2.
- Provide good documentation, independent of the SDL2 documentation.
- Cover as much of the SDL2 API as possible, excluding elements of the API that
  do not provide value to a program written in Python (e.g. thread management
  and shared object loading).

An explicit anti-goal of sdl2hl is providing any significant functionality beyond
that which is provided by SDL2. sdl2hl may be a reasonable foundation of a
larger game library, but it will not become one itself.

Versioning
----------

sdl2hl versioning follows the semver 2.0 standard. Once sdl2hl hits 1.0, every
effort will be made to prevent backwards incompatible changes. If a backwards
incompatible change absolutely cannot be avoided, sdl2hl's major version will be
incremented. However, since sdl2hl has not hit 1.0, for now there may be
breaking changes at any time. Sorry.

License
-------

sdl2hl is licensed under the same zlib license as SDL2 and sdl2-cffi. More
details can be found in the LICENSE.txt file that (should) be found in this
distribution.

Contributions
-------------

Contributions are welcome! If you encounter a bug or have a request or
suggestion please open an issue on github at
https://github.com/jdoda/sdl2hl/issues . If you want to submit a patch, please
open a github pull request at https://github.com/jdoda/sdl2hl/pulls .

Example
-------

.. code:: python

	import sys

	import sdl2hl


	BACKGROUND_COLOR = (0,0,0,255)
	AVATAR_COLOR = (255,0,0,255)


	sdl2hl.init()
	window = sdl2hl.Window()
	renderer = sdl2hl.Renderer(window)
	avatar = sdl2hl.Rect(w=64, h=64)

	while True:
	    for event in sdl2hl.events.poll():
		if event.type == sdl2hl.QUIT:
		    sdl2hl.quit()
		    sys.exit()
		elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_LEFT:
		    avatar.x -= 1
		elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_RIGHT:
		    avatar.x += 1
		elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_UP:
		    avatar.y -= 1
		elif event.type == sdl2hl.KEYDOWN and event.keysym.sym == sdl2hl.K_DOWN:
		    avatar.y += 1

	    renderer.draw_color = BACKGROUND_COLOR
	    renderer.clear()
	    renderer.draw_color = AVATAR_COLOR
	    renderer.fill_rect(avatar)

	    renderer.present()
