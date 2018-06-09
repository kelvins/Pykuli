#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time

from pykeyboard import PyKeyboard
from pymouse import PyMouse


class Pykuli(object):

    def __init__(self, default_path=u''):
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.default_path = default_path

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)

    def _mouse_move(self, x, y):
        self.mouse.move(x, y)

    def _mouse_click(self, x, y):
        self.mouse.click(x, y)
