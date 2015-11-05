#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    This script is based on script.randomitems & script.wacthlist
#    Thanks to their original authors

import xbmc
import xbmcaddon

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')

def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGNOTICE)

class MediaTypes:
    MOVIE = "MOVIE"
    AUDIO = "AUDIO"
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

class Main:
    def __init__(self):
        self.playerEventReceiver = PlayerEventReceiver()
        self._daemon()
        
    def _daemon(self):
        while not xbmc.abortRequested:
            xbmc.sleep(1000)
        log('abort requested')
        
class PlayerEventReceiver(xbmc.Player):
    curMediaType = None
    
    def _sendSignal(self, event):
        mediaType = self._getMediaType()
        
        if event == EventNames.PLAYING:
            self.curMediaType = mediaType
        elif event == EventNames.STOPPED:
            mediaType = self.curMediaType
            self.curMediaType = None
    
        if not MediaTypes.isVideo(mediaType):
            log("Non-video media played, not sending any signals: " + mediaType)
            return

        stereoscopic = self._getStereoscopicMode()
        aspectRatio = self._getAspectRatio()
        
        log("Sending {event}, {mediaType!r} {aspectRatio!r} {stereoscopic!r}".format(event=event, mediaType=mediaType, aspectRatio=aspectRatio, stereoscopic=stereoscopic))

    def _getStereoscopicMode(self):
        return StereoscopicModes.getMode(xbmc.getInfoLabel('VideoPlayer.StereoscopicMode'))
        
    def _getAspectRatio(self):
        return xbmc.getInfoLabel('VideoPlayer.VideoAspect') or AspectRatios.DEFAULT
        
    def _getMediaType(self):
        mediaType = MediaTypes.UNKNOWN

        if self.isPlayingAudio():
            mediaType = MediaTypes.MUSIC
        elif self.isPlayingVideo():
            
            for i in range(10):
                if xbmc.getInfoLabel('VideoPlayer.Title') != '':
                    break

                log("Player is not ready on attempt {}, waiting 10ms and trying again".format(i))
                xbmc.sleep(10)

            if xbmc.getCondVisibility('VideoPlayer.Content(movies)'):
                try:
                    filename = self.getPlayingFile()
                    if '-trailer' in filename:
                        mediaType = MediaTypes.TRAILER
                    elif filename.startswith('http://') or filename.startswith('https://'):
                        mediaType = MediaTypes.TRAILER
                    else:
                        mediaType = MediaTypes.MOVIE
                except:
                    log("Exception trying to get the current filename")
                    pass
            elif xbmc.getCondVisibility('VideoPlayer.Content(episodes)') and xbmc.getInfoLabel('VideoPlayer.Season') != '' and xbmc.getInfoLabel('VideoPlayer.TVShowTitle') != '':
                mediaType = MediaTypes.EPISODE
            else:
                mediaType = MediaTypes.VIDEO
        else:
            log('Unknown media type currently playing')
            
        return mediaType

    def onPlayBackStarted(self):
        self._sendSignal(EventNames.PLAYING)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    def onPlayBackStopped(self):
        self._sendSignal(EventNames.STOPPED)

    def onPlayBackPaused(self):
        self._sendSignal(EventNames.PAUSED)

    def onPlayBackResumed(self):
        self._sendSignal(EventNames.RESUMED)

if __name__ == "__main__":
    log('script version %s started' % __addonversion__)
    Main()
    log('script version %s stopped' % __addonversion__)
