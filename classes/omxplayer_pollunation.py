import pexpect
import re

from threading import Thread
#from time import sleep
import time

class OMXPlayer(object):

    _SCREEN_SIZE_CMD = "fbset -s | grep geometry|awk '{print $2, $3}'"
    
    _MEDIA_LEN_REXP = re.compile(r".*Duration: (\d+):(\d+):(\d+(.\d+)?),.*")
    _FILEPROP_REXP  = re.compile(r".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP    = re.compile(r"A:\s*-?([\d.]+).*")
    _DONE_REXP      = re.compile(r"have a nice day.*")

    _LAUNCH_CMD     = '/usr/bin/omxplayer -s %s %s'
    _PAUSE_CMD      = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD       = 'q'
    _RESTART_CMD    = 'i'

    _MEDIA_LENGTH_TH  = 1
    paused            = False
    subtitles_visible = True
    kill_self         = False
    
    def __init__(self, mediafile, loop=False, args="", start_playback=False, debug=0):
        args += " --no-osd"
        self.debug = debug
        self.loop = loop
        self.start_playback = start_playback

        if self.debug:
            print 'DEBUG'
            import os
            screen_size = os.popen(self._SCREEN_SIZE_CMD).read().split()
            w = int(screen_size[0]); h = int(screen_size[1])
            args += " --win {0},{1},{2},{3} ".format(int(w/2),int(h/2),int(w/4+w/2),int(h/4+h/2))
        if self.loop:
            args += " --loop "
        
        self.media_len = self.getMediaLength(mediafile)

        self._position_thread = None
        self._loop_thread     = None
        
        self.cmd = self._LAUNCH_CMD % (mediafile, args)
        self.start_proc()

    def start_proc(self):
        if self.debug:
            print 'Starting omxplayer process'
        self._process = pexpect.spawn(self.cmd)
        
        self.video = dict()
        self.audio = dict()

        self.time_till_pause = 0
        self.time_of_play = time.time()              
        self.position = 0
        time.sleep(0.2)
        if not self.start_playback:
            self.pause()
        else:
            self.play()

        if  self._position_thread is None:
            self._position_thread = Thread(target=self._get_position)
            self._position_thread.start()
        if  self._loop_thread     is None:
            self._loop_thread     = Thread(target=self._do_loop)
            self._loop_thread.start()

    def _get_position(self):
        while not self.kill_self:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            if self.debug>0 and index>0:
                print 'index == {}'.format(index)
            if index == 1: continue
            elif index in (2, 3):
                self.paused = True
                break
            else:
                pos = float(self._process.match.group(1))
                self.time_till_pause = pos
                self.time_of_play = time.time()
                if self.debug>1:
                    print 'Position: {}'.format(self.position)

            time.sleep(0.05)

    def _do_loop(self):
        while not self.kill_self: # self._process.isalive():            
            if self.paused:
                continue
            elif self.loop and not self._process.isalive():
                print 'DIED'
                self.play()

            self.position = self.time_till_pause + (time.time() - self.time_of_play)
            if self.debug > 1:
                print 'Position: {}'.format(self.position)
            if self.position >= self.media_len - self._MEDIA_LENGTH_TH:
                if self.debug:
                    print 'Reached End (almost): {0}'.format(self.position)
                if not self.loop:
                    self.pause()
                    time.sleep(0.01)
                    self.restart()
                #if self.loop:
                #    self.play()

            time.sleep(0.05)
            
    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused
            if self.paused:
                self.time_till_pause = self.position
            else:
                self.time_of_play = time.time()              
            
    def play(self):
        if not self._process.isalive():
            self.start_proc()
        if self.paused:
            self.toggle_pause()

    def pause(self):
        if not self.paused:
            self.toggle_pause()

    def stop(self):
        print 'Stop'
        self._process.send(self._QUIT_CMD)
        # tell position Thread to kill itself as well
        self.kill_self = True
        while self._process.isalive():
            print 'still alive!!!'
            self._process.terminate(force=True)

    def restart(self):
        self._process.send(self._RESTART_CMD)
        self.time_till_pause = 0
        self.time_of_play = time.time()

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError

    def getMediaLength(self, mediafile):
        cmd = self._LAUNCH_CMD % (mediafile, '-i')
        self._process = pexpect.spawn(cmd)
        line=self._process.readline()
        while line:
            check = self._MEDIA_LEN_REXP.match(line)
            if check:
                h = check.group(1)
                m = check.group(2)
                s = check.group(3)
                return float(s) + float(m)*60 + float(h)*60*60
            line=self._process.readline()
                
