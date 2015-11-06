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

