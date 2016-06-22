#--------------------------------------------
# Time constants (all times are in seconds):
#--------------------------------------------
PAUSE_TIME = 3 # if the advisor GPIO input pin is low for shorter than this time, the advisor will continue from the same place
DELAY_TIME = 3 # the time by which the video play will be delayed after the GPIO input pin rising edge

POLLING_DELAY = 0.005 # time between gpio input polling tries
POLLING_TRIES = 20    # number of tries with the same gpio value after change to consider it stable (debouncing)

#---------------------------------------------------
#select movie - leave exactly one line un-commented:
#---------------------------------------------------
movie = r'/home/pi/Downloads/eyal_kimchi.mp4'
#movie = r'/home/pi/Downloads/uri_ariel.mp4'
#movie = r'/home/pi/Downloads/market_intreviews.mp4'
#movie = r'/home/pi/Downloads/dan_levanon.mp4'
