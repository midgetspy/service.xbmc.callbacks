service.xbmc.callbacks
======================

Calls a script whenever an event occurs in XBMC and pass it arguments to indicate what event has occurred. All invocations will have an event argument:

--event= PLAYING, PAUSED, RESUMED, STOPPED, IDLE, NOT_IDLE, SCREENSAVER_ACTIVATED, SCREENSAVER_DEACTIVATED, DATABASE_UPDATED

Additional arguments will be provided if the event name is PLAYING, PAUSED, RESUMED, or STOPPED:

--mediaType= MOVIE, MUSIC, EPISODE, VIDEO, TRAILER, UNKNOWN

If the media type is MOVIE, EPISODE, VIDEO, or TRAILER then the additional arguments will be provided:

--stereoscopicMode= 2D, HSBS

--aspectRatio= DEFAULT, 1.33, 1.37, 1.66, 1.78, 1.85, 2.20, 2.35, 2.40, 2.55, 2.76


The resources/lib folder contains an example of how to parse these arguments in python (and a batch file which can call the python file under windows).