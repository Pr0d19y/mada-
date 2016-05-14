import RPi.GPIO as GPIO
import sys
import os
import subprocess
from classes.omxplayer import OMXDriver

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

movie1 = ("/opt/vc/src/hello_pi/hello_video/test.h264")

last_state1 = True
last_state2 = True

input_state1 = True
input_state2 = True

quit_video = True
player = False

while True:  
	#Read states of inputs  
	input_state1 = GPIO.input(17)
	omx = OMXDriver(1)
	input_state2 = GPIO.input(18)
	#print input_state2,last_state2
	quit_video = GPIO.input(24)
	#If GPIO(17) is shorted to ground
	if input_state1 != last_state1:
		if (player and not input_state1):
			os.system('killall omxplayer.bin')
			#omxc = subprocess.Popen(['omxplayer', '-b', movie1], stdin=subprocess.PIPE)
			omx.play(movie1,"")
			player = True
		elif not input_state1:
			#omxc = subprocess.Popen(['omxplayer', '-b', movie1], stdin=subprocess.PIPE)
			omx.play(movie1,"")
			player = True
	elif input_state2 != last_state2:
		if player and not input_state2:
			#omxc.stdin.write('q')
			print "stopping"
			print omx.is_running
			omx.pause
			player = False
	
	if quit_video == False:
		os.system('killall omxplayer.bin')
		player = False

	#Set last_input states
	last_state1 = input_state1
	last_state2 = input_state2 
