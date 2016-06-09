import time

## Female ##

# Set Video Files
idle_video = '/home/pi/Haavaka/avkanim_blink.mp4'

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
  

# This is the old code
while False:
    male_pre.play()
    is_bee_catched = False
    catch_time = 0
    while catch_time < CATCH_TIME_TH:
        while not input(bee_catch):
            output(bee_vibrate, False)
            pass
        start_time = time.time()
        while input(bee_catch):
            output(bee_vibrate, True)
            pass
        end_time  = time.time()
        catch_time = end_time - start_time
    
    is_bee_catched = True
    
    output(fem_catch, True)
    male_pre.pause()
    male_post.play()

    while not fem_release:
        pass
    male_post.pause()
