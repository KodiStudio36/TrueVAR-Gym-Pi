class Cam:

    def __init__(self):
        pass

    def get_source(self):
        return ['videotestsrc', '!', 'video/x-raw,width=1264,height=711,framerate=30/1,format=RGBA,interlace-mode=progressive']