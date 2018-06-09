#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time

from pykeyboard import PyKeyboard
from pymouse import PyMouse
from PIL import Image
from mss import mss
from template_match import template_match

import pykuli_exceptions


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

    @staticmethod
    def take_screenshot():
        with mss() as sct:
            # Get a screenshot of the 1st monitor
            sct_img = sct.grab(sct.monitors[1])

            # Create an Image
            img = Image.new('RGB', sct_img.size)

            # Best solution: create a list(tuple(R, G, B), ...) for putdata()
            pixels = zip(sct_img.raw[2::4],
                         sct_img.raw[1::4],
                         sct_img.raw[0::4])

            img.putdata(list(pixels))

            return img

    def click(self, image_path):

        try:
            image = Image.open(self.default_path + image_path)
            image = image.convert("RGB")
            screenshot = self.take_screenshot()
            x, y = template_match(screenshot, image)
            self._mouse_move(x, y)
            self._mouse_click(x, y)
        except pykuli_exceptions.NoMatchException as err:
            print err
        except Exception as err:
            print err


if __name__ == u'__main__':
    p = Pykuli(u'../')
    p.click(u'teste2.png')
