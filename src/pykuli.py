#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import time

from pykeyboard import PyKeyboard
from pymouse import PyMouse
from mss import mss
from PIL import Image


class Pykuli(object):

    SCREENSHOT_NAME = u'monitor-1.png'

    def __init__(self, default_path=u''):
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.default_path = default_path

    def __del__(self):
        os.remove(u'monitor-1.png')

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)

    def _mouse_move(self, x, y):
        self.mouse.move(x, y)

    def _mouse_click(self, x, y):
        self.mouse.click(x, y)

    def _take_screenshot(self):
        with mss() as screen:
            screen.shot()
        return self._load_image(self.SCREENSHOT_NAME)

    def _load_image(self, image_path):
        return Image.open(image_path)
