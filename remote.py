

import sys
import glob
import time
from enum import Enum

from lib import *

import serial
from serial.threaded import LineReader, ReaderThread

buttons = Enum('Button', 'up right down left center menu')

class AppleRemote(ReaderThread):

    def __init__(self, device=None):
        if device is None:
            device = glob.glob('/dev/tty.usb*')[0]

        ser = serial.Serial(device, 9600, timeout=0)
        ar = self

        self.pending = None
        self.handlers = [print]

        class PrintLines(LineReader):
            def connection_made(self, transport):
                super(PrintLines, self).connection_made(transport)
                sys.stdout.write('port opened\n')

            def handle_line(self, data):
                if data == '26738':
                    btn = buttons.up
                elif data == '28786':
                    btn = buttons.right
                elif data == '22642':
                    btn = buttons.down
                elif data == '2162':
                    btn = buttons.left
                elif data == '4210':
                    btn = buttons.center
                elif data == '8306':
                    btn = buttons.menu
                else:
                    return

                for handler in ar.handlers:
                    handler(btn)
                
                ar.pending = btn

            def connection_lost(self, exc):
                sys.stdout.write('port closed\n')

        super(AppleRemote, self).__init__(ser, PrintLines)


    def attach_handler(self, handler):
        if self.handlers[0] == print:
            self.handlers = []
        self.handlers.append( handler )

    def await_btn(self):
        self.pending = None
        while self.pending is None:
            sleep(0.01)

        detected = self.pending
        return detected