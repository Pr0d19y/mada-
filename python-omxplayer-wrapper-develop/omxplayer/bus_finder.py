import os.path
import time
from glob import glob
from logging import getLogger

logger = getLogger(__name__)


class BusFinder(object):
    def __init__(self, path=None, pidpath=None):
        self.path = path
        self.pidpath = pidpath
        logger.debug('BusFinder initialised with path: %s' % path)

    def get_address(self):
        self.wait_for_file()
        logger.debug('Opening file at %s' % self.path)
        with open(self.path, 'r') as f:
            logger.debug('Opened file at %s' % self.path)
            self.address = f.read().strip()
            logger.debug('Address \'%s\' parsed from file' % self.address)
        return self.address

    def get_process(self):
        self.wait_for_process_file()
        logger.debug('Opening file at %s' % self.pidpath)
        with open(self.pidpath, 'r') as f:
            logger.debug('Opened file at %s' % self.pidpath)
            self.pid = int(f.read().strip())
            logger.debug('Process ID \'%s\' parsed from file' % self.pid)
        return self.pid

    def find_address_file(self):
        """
        Finds the OMXPlayer DBus connection
        Assumes there is an alive OMXPlayer process.
        :return:
        """
        possible_address_files = []
        while not possible_address_files:
            # filter is used here as glob doesn't support regexp :(
            isnt_pid_file = lambda path: not path.endswith('.pid')
            possible_address_files = list(filter(isnt_pid_file,
                                            glob('/tmp/omxplayerdbus.*')))
            possible_address_files.sort(key=lambda path: os.path.getmtime(path))
            time.sleep(0.05)

        self.path = possible_address_files[-1]

    def find_process_file(self):
        """
        Finds the OMXPlayer DBus Process
        Assumes there is an alive OMXPlayer process.
        :return:
        """
        possible_pid_files = []
        while not possible_pid_files:
            # filter is used here as glob doesn't support regexp :(
            is_pid_file = lambda path: path.endswith('.pid')
            possible_pid_files = filter(is_pid_file,
                                            glob('/tmp/omxplayerdbus.*'))
            possible_pid_files.sort(key=lambda path: os.path.getmtime(path))
            time.sleep(0.05)

        self.pidpath = possible_pid_files[-1]

    def wait_for_path_to_exist(self):
        while not os.path.isfile(self.path):
            time.sleep(0.05)

    def wait_for_dbus_address_to_be_written_to_file(self):
        while not os.path.getsize(self.path):
            time.sleep(0.05)

    def wait_for_file(self):
        if self.path:
            self.wait_for_path_to_exist()
        else:
            self.find_address_file()
        self.wait_for_dbus_address_to_be_written_to_file()

    def wait_for_process_file_to_exist(self):
        while not os.path.isfile(self.pidpath):
            time.sleep(0.05)

    def wait_for_process_to_be_written_to_file(self):
        while not os.path.getsize(self.pidpath):
            time.sleep(0.05)

    def wait_for_process_file(self):
        if self.pidpath:
            self.wait_for_process_file_to_exist()
        else:
            self.find_process_file()
        self.wait_for_process_to_be_written_to_file()
