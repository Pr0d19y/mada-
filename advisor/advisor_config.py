# Time constants (all times are in seconds):
PAUSE_TIME = 2 # if the advisor GPIO input pin is low for shorter than this time, the advisor will continue from the same place
DELAY_TIME = 1 # the time by which the video play will be delayed after the GPIO input pin rising edge

POLLING_DELAY = 0.005 # time between gpio input polling tries
POLLING_TRIES = 20    # number of tries with the same gpio value after change to consider it stable (debouncing)
