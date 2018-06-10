#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The Pykuli project is inspired by Sikuli.
With the Pykuli class you can automate everything you see.
"""
import time

from pykeyboard import PyKeyboard
from pymouse import PyMouse
from PIL import Image
from mss import mss
from template_match import template_match

import pykuli_exceptions


class Pykuli(object):
    """
    Pykuli class is the main class from the Pykuli project.

    Args:
        default_path (str): the default path where the images are.
    """

    def __init__(self, default_path=u''):
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.default_path = default_path

    @staticmethod
    def wait(seconds):
        """
        Wait method is just a wrapper for the time.sleep function.

        Args:
            seconds (int): seconds to sleep.
        """
        time.sleep(seconds)

    @staticmethod
    def take_screenshot():
        """
        This method uses the mss package to take a screen shot
        of the screen and return a Pillow format image.

        Return:
            A Pillow image.
        """
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
        """
        This is one of the main class of the project.
        By using this class the user can click on a specific
        location of the screen, based on the image passed by parameter.

        Args:
            image_path (str): path to the image we want to match.
            Note that this will be concatenated to the default_path.
        """

        try:
            image = Image.open(self.default_path + image_path)
            image = image.convert("RGB")
            screenshot = self.take_screenshot()
            x, y = template_match(screenshot, image)
            self.mouse.move(x, y)
            self.mouse.click(x, y)
        except pykuli_exceptions.NoMatchException as err:
            print err
        except Exception as err:
            print err


if __name__ == u'__main__':
    p = Pykuli(u'../')
    p.click(u'teste.png')
