

    >>> import adventure
    >>> adventure.play()
    WELCOME TO ADVENTURE!!  WOULD YOU LIKE INSTRUCTIONS?

    >>> no
    YOU ARE STANDING AT THE END OF A ROAD BEFORE A SMALL BRICK BUILDING.
    AROUND YOU IS A FOREST.  A SMALL STREAM FLOWS OUT OF THE BUILDING AND
    DOWN A GULLY.

    >>> east
    YOU ARE INSIDE A BUILDING, A WELL HOUSE FOR A LARGE SPRING.
    THERE ARE SOME KEYS ON THE GROUND HERE.
    THERE IS A SHINY BRASS LAMP NEARBY.
    THERE IS FOOD HERE.
    THERE IS A BOTTLE OF WATER HERE.

    >>> get(lamp)
    OK

    >>> leave
    YOU'RE AT END OF ROAD AGAIN.

    >>> south
    YOU ARE IN A VALLEY IN THE FOREST BESIDE A STREAM TUMBLING ALONG A
    ROCKY BED.


You can save your game at any time by calling the ``save()`` command
with a filename, and then can resume it later::

    >>> save('advent.save')
    GAME SAVED

    >>> adventure.resume('advent.save')
    GAME RESTORED
    >>> look
    SORRY, BUT I AM NOT ALLOWED TO GIVE MORE DETAIL.  I WILL REPEAT THE
    LONG DESCRIPTION OF YOUR LOCATION.
    YOU ARE IN A VALLEY IN THE FOREST BESIDE A STREAM TUMBLING ALONG A
    ROCKY BED.



Notes
=====

* Several Adventure commands conflict with standard Python built-in
  functions.  If you want to run the normal Python function ``exit()``,
  ``open()``, ``quit()``, or ``help()``, then import the ``builtin``
  module and run the copy of the function stored there.

* The word “break” is a Python keyword, so there was no possibility of
  using it in the game.  Instead, use one of the two synonyms defined by
  the PDP version of Adventure: “shatter” or “smash.”
