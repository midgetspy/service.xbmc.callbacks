import getopt
import sys

long_args, args = getopt.getopt(sys.argv[1:], "", longopts=["event=", "mediaType=", "aspectRatio=", "stereoscopic="])
print dict(map(lambda x: (x[0].lstrip('-'), x[1]), long_args))