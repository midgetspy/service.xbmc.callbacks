# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://github.com/midgetspy/service.xbmc.callbacks

class MediaTypes:
    MOVIE = "MOVIE"
    MUSIC = "MUSIC"
    EPISODE = "EPISODE"
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    UNKNOWN = "UNKNOWN"
    
    @staticmethod
    def isVideo(mediaType):
        return mediaType in (MediaTypes.MOVIE, MediaTypes.EPISODE, MediaTypes.VIDEO, MediaTypes.TRAILER)

class StereoscopicModes:
    NONE = "2D"
    HSBS = "HSBS"
    
    @staticmethod
    def getMode(xbmcValue):
        if xbmcValue == '':
            return StereoscopicModes.NONE
        elif xbmcValue == 'left_right':
            return StereoscopicModes.HSBS

class AspectRatios:
    DEFAULT = 'DEFAULT'
    # 1.33, 1.37, 1.66, 1.78, 1.85, 2.20, 2.35, 2.40, 2.55, 2.76

class EventNames:
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    RESUMED = "RESUMED"
    STOPPED = "STOPPED"
    IDLE = "IDLE"
    NOT_IDLE = "NOT_IDLE"
    SCREENSAVER_ACTIVATED = "SCREENSAVER_ACTIVATED" 
    SCREENSAVER_DEACTIVATED = "SCREENSAVER_DEACTIVATED"
    DATABASE_UPDATED = "DATABASE_UPDATED"
