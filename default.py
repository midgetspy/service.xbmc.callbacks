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

import subprocess
import traceback

import xbmc
import xbmcaddon

from resources.lib.common import MediaTypes, EventNames, StereoscopicModes, AspectRatios

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')

class Logger(object):
    @staticmethod
    def _log(txt, log_level=xbmc.LOGNOTICE, *args, **kwargs):
        if args or kwargs:
            txt = txt.format(*args, **kwargs)
        message = "{addonName}: {message}".format(addonName=__addonname__, message=txt.encode('ascii', 'ignore'))
        xbmc.log(msg=message, level=log_level)
    
    @staticmethod
    def info(txt, *args, **kwargs):
        Logger._log(txt, xbmc.LOGINFO, *args, **kwargs)
    
    @staticmethod
    def debug(txt, *args, **kwargs):
        Logger._log(txt, xbmc.LOGDEBUG, *args, **kwargs)
    
    @staticmethod
    def notice(txt, *args, **kwargs):
        Logger._log(txt, xbmc.LOGNOTICE, *args, **kwargs)
        
    @staticmethod
    def warning(txt, *args, **kwargs):
        Logger._log(txt, xbmc.LOGWARNING, *args, **kwargs)

def call_script(*args, **kwargs):
    callbackScript = xbmc.translatePath(__addon__.getSetting("callback_script"))
    
    if not callbackScript:
        Logger.warning("No script defined, unable to send callback")
        return
    
    call_args = [callbackScript]
    call_args += args
    
    for keyword in kwargs.keys():
        call_args.append('--{key}={value}'.format(key=keyword, value=kwargs[keyword]))
    
    try:
        Logger.notice("Calling script: {}", call_args)
        p = subprocess.Popen(call_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            Logger.notice("Result: {}", out)
        if err:
            Logger.warning("Error: {}", err)
    except Exception as e:
        Logger.warning("Error when trying to execute script: {}", e)
        Logger.debug(traceback.format_exc(e))

class PlayerEventReceiver(xbmc.Player):
    curMediaType = None
    
    def _sendEvent(self, event):

        args = {'event': event}
       
        mediaType = self._getMediaType()
        
        if event == EventNames.PLAYING:
            self.curMediaType = mediaType
        elif event == EventNames.STOPPED:
            mediaType = self.curMediaType
            self.curMediaType = None

        args['mediaType'] = mediaType
    
        if MediaTypes.isVideo(mediaType):
            args['stereoscopic'] = self._getStereoscopicMode() 
            args['aspectRatio'] = self._getAspectRatio()
        
        call_script(**args)

    def _getStereoscopicMode(self):
        return StereoscopicModes.getMode(xbmc.getInfoLabel('VideoPlayer.StereoscopicMode'))
        
    def _getAspectRatio(self):
        return xbmc.getInfoLabel('VideoPlayer.VideoAspect') or AspectRatios.DEFAULT
        
    def _getMediaType(self):
        mediaType = MediaTypes.UNKNOWN

        if self.isPlayingAudio():
            mediaType = MediaTypes.MUSIC
        elif self.isPlayingVideo():
            
            # sometimes the player says it's playing a video but doesn't actually return the correct info for the video that
            # is playing. If we wait until VideoPlayer.Title is populated it seems to be mostly consistent. Sometimes the
            # aspect ratio is still wrong though.
            for i in range(10):
                if xbmc.getInfoLabel('VideoPlayer.Title') != '':
                    break

                Logger.notice("Player is not ready on attempt {}, waiting 10ms and trying again", i)
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
                    Logger.notice("Exception trying to get the current filename")
                    pass
            elif xbmc.getCondVisibility('VideoPlayer.Content(episodes)') and xbmc.getInfoLabel('VideoPlayer.Season') != '' and xbmc.getInfoLabel('VideoPlayer.TVShowTitle') != '':
                mediaType = MediaTypes.EPISODE
            else:
                mediaType = MediaTypes.VIDEO
        else:
            Logger.notice('Unknown media type currently playing')
            
        return mediaType

    def onPlayBackStarted(self):
        self._sendEvent(EventNames.PLAYING)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    def onPlayBackStopped(self):
        self._sendEvent(EventNames.STOPPED)

    def onPlayBackPaused(self):
        self._sendEvent(EventNames.PAUSED)

    def onPlayBackResumed(self):
        self._sendEvent(EventNames.RESUMED)

class MyMonitor(xbmc.Monitor):

  def onScreensaverActivated(self):
      call_script({'event': EventNames.SCREENSAVER_ACTIVATED})

  def onScreensaverDeactivated(self):
      call_script({'event': EventNames.SCREENSAVER_DEACTIVATED})

  def onDatabaseUpdated(self, db):
      call_script({'event': EventNames.DATABASE_UPDATED})

if __name__ == "__main__":
    Logger.notice('Script version {} started', __addonversion__)
    
    # make a player that will get called when media-related things happen
    playerEventReceiver = PlayerEventReceiver()
    monitor = MyMonitor()
    
    sent_idle = False

    # block here so the script stays active until XBMC shuts down
    while not xbmc.abortRequested:

        # watch for the idle time to cross the threshold and send the idle event when it does        
        if xbmc.getGlobalIdleTime() > 60 * int(__addon__.getSetting("idle_time")):
            if not sent_idle:
                call_script({'event': EventNames.IDLE})
                sent_idle = True
        else:
            if sent_idle:
                call_script({'event': EventNames.NOT_IDLE})
                sent_idle = False
        xbmc.sleep(1000)
    
    Logger.notice('Script version {} stopped', __addonversion__)
