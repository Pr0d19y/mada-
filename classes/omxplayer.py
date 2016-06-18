import pexpect
import re
import logging
import sys

from threading import Thread
#from time import sleep
import time

class OMXPlayer(object):

    _MEDIA_LEN_REXP = re.compile(r".*Duration: (\d+):(\d+):(\d+(.\d+)?),.*")
    _FILEPROP_REXP  = re.compile(r".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP    = re.compile(r"V :\s*([\d.]+).*")
    _DONE_REXP      = re.compile(r"have a nice day.*")

    #_LAUNCH_CMD     = '/usr/bin/omxplayer -s %s %s'
    _LAUNCH_CMD     = '/usr/bin/omxplayer %s %s'
    _PAUSE_CMD      = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD       = 'q'
    _RESTART_CMD    = 'i'

    _MEDIA_LENGTH_TH  = 0.5
    paused            = False
    subtitles_visible = True

    def __init__(self, mediafile, loop=False, args="", start_playback=False):
        #args += " --no-osd"
        self.logger = logging.getLogger('omxplayerLogger')
        self.loop = loop
            
        self.media_len = self.getMediaLength(mediafile)
        cmd = self._LAUNCH_CMD % (mediafile, args)
        self.logger.info('starting omxplayer with command: {}'.format(cmd))
        self._process = pexpect.spawn(cmd)
        f = open('pexpect_log_file', 'w')
        self._process.logfile = f
        
        self.video = dict()
        self.audio = dict()
        # Get file properties
        #file_props = self._FILEPROP_REXP.match(self._process.readline()).groups()
        #(self.audio['streams'], self.video['streams'],
        # self.chapters, self.subtitles) = [int(x) for x in file_props]
        # Get video properties
        #video_check = self._VIDEOPROP_REXP.match(self._process.readline())
        #if video_check:
        #    video_props = video_check.groups()
        #    self.video['decoder'] = video_props[0]
        #    self.video['dimensions'] = tuple(int(x) for x in video_props[1:3])
        #    self.video['profile'] = int(video_props[3])
        #    self.video['fps'] = float(video_props[4])
        #else:
        #    print "Error parsing video properties"
        # Get audio properties
        #audio_check = self._AUDIOPROP_REXP.match(self._process.readline())
        #if audio_check:
        #    audio_props = audio_check.groups()
        #    self.audio['decoder'] = audio_props[0]
        #    (self.audio['channels'], self.audio['rate'],
        #     self.audio['bps']) = [int(x) for x in audio_props[1:]]
        #else:
        #    print "Error parsing audio properties"


        #if self.audio['streams'] > 0:
        #    self.current_audio_stream = 1
        #    self.current_volume = 0.0

        #self.time_till_pause = 0
        #self.time_of_play = time.time()
        #self.position = 0
        time.sleep(0.2)
        if not start_playback:
            self.pause()
        else:
            self.play()

        # self._position_thread = Thread(target=self._get_position)
        # self._position_thread.setDaemon(True)
        # self._position_thread.start()

    def _get_position___old____(self):
        
        while True:
            self.logger.debug('Getting position')
            #print 'Getting position'
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            self.logger.debug('index == {}'.format(index))
            #print 'index == {}'.format(index)
            if index == 1: continue
            elif index in (2, 3): break
            else:
                self.position = float(self._process.match.group(1))
                #self.logger.debug('Position: {}'.format(self.position))
                #print 'Position: {}'.format(self.position)

            if self.position >= self.media_len - self._MEDIA_LENGTH_TH:
                self.logger.debug('Reached End (almost)')
                #print 'Reached End (almost)'
                if not self.loop:
                    self.pause()
                self.restart()
                #self.position = 0
                    
            time.sleep(0.05)

    def _get_position(self):
        self.logger.debug('_get_position STARTED')
        while True:
            if not self._process.isalive():
                return
            if self.paused:
                continue

            self.position = self.time_till_pause + (time.time() - self.time_of_play)
            #print 'Position: {}'.format(self.position)
            #self.logger.debug('Position: {}'.format(self.position))
            if self.position >= self.media_len - self._MEDIA_LENGTH_TH:
                #print 'Reached End (almost)'
                self.logger.debug('Reached End (almost)')
                if not self.loop:
                    self.pause()
                    time.sleep(0.01)
                self.restart()

            time.sleep(0.05)

    def toggle_pause(self):
        self.logger.debug('in toggle_pause')
        self._process.send(self._PAUSE_CMD)
        self.paused = not self.paused
        if self.paused:
            self.logger.debug('now movie should be PAUSED')
            #self.time_till_pause = self.position
        else:
            self.logger.debug('now movie should be RUNNING')
            #self.time_of_play = time.time()
            
    def play(self):
        self.logger.debug('in play')
        if self.paused:
            self.toggle_pause()

    def pause(self):
        self.logger.debug('in pause')
        if not self.paused:
            self.toggle_pause()

    def stop(self):
        self.logger.debug('in stop')
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def seek_0(self):
        self.logger.debug('in seek_0')
        self._process.send(self._RESTART_CMD)

    def restart(self):
        self.logger.debug('in restart')
        self.logger.debug('in restart')

        a = self._process.send(self._RESTART_CMD)
        self.logger.debug('process respond: {}'.format(a))
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
        self.logger.debug('in getMediaLength')
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
