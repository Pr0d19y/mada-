import time

## Female ##

# Set Video Files
idle_video = '/home/pi/mada-/pollunation/videos/tzaleket_blink_00.mp4'
dust_complete_video = '/home/pi/mada-/pollunation/videos/tzaleket_after_00.mp4'

# Set GPIO names
bee_on        = 38
wait_for_bee  = 31
flag_male     = 37

setup(bee_lights,  OUT)
setup(bee_catch,   IN, pull_up_down=PUD_DOWN)
setup(fem_release, IN, pull_up_down=PUD_DOWN)
setup(fem_catch,   OUT)

output(fem_catch,   False)

if female:

  def state_idle():
    output(flag_male, False)
    play_video(idle_video, loop=True)
    while True:
      if input(wait_for_bee):
        return(state_wait_for_bee)

  def state_wait_for_bee():
    output(flag_male, False)
    # play_video(idle_video, loop=True)
    while True:
      if input(bee_on):
        return state_bee_on

  def state_bee_on():
    output(flag_male, False)
    # play_video(idle_video, loop=True)
    start_time = time.time()
    while  True:
      if not input(bee_on):
        return state_wait_for_bee
      if (time.time() - start_time)>= BEE_TIME_TH:
        return state_dust_complete

  def state_dust_complete():
    output(flag_male, True)
    play_video(dust_complete_video, wait=True)
    return state_idle
  
