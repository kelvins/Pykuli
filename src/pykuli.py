#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The Pykuli project is inspired by Sikuli.
With the Pykuli class you can automate everything you see.
"""
import time
import logging
from logging.config import fileConfig
from datetime import datetime, timedelta

from mss import mss
from PIL import Image
from pymouse import PyMouse
from pykeyboard import PyKeyboard

import pykuli_exceptions
from template_match import template_match

fileConfig(u'logging_config.ini')


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
        self.logger = logging.getLogger()

    def press_key(self, key):
        """
        Wrapper for the PyKeyboard press_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'PRESS KEY "%s"', key)
        self.keyboard.press_key(key)

    def release_key(self, key):
        """
        Wrapper for the PyKeyboard release_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'RELEASE KEY "%s"', key)
        self.keyboard.release_key(key)

    def tap_key(self, key):
        """
        Wrapper for the PyKeyboard tap_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'TAP KEY "%s"', key)
        self.keyboard.tap_key(key)

    def type_string(self, string):
        """
        Wrapper for the PyKeyboard type_string method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'TYPE STRING "%s"', string)
        self.keyboard.type_string(string)

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
            img = Image.new(u'RGB', sct_img.size)

            # Best solution: create a list(tuple(R, G, B), ...) for putdata()
            pixels = zip(sct_img.raw[2::4],
                         sct_img.raw[1::4],
                         sct_img.raw[0::4])

            img.putdata(list(pixels))

            return img

    def click(self, image_path, seconds=0):
        """
        This is one of the main class of the project.
        By using this class the user can click on a specific
        location of the screen, based on the image passed by parameter.

        Args:
            image_path (str): path to the image we want to match.
            Note that this will be concatenated to the default_path.
            seconds (int): seconds to wait for the image to appear.
        """

        datetime_limit = datetime.now() + timedelta(seconds=seconds)
        last_datetime = None

        while True:
            try:
                if last_datetime and last_datetime > datetime_limit:
                    self.logger.warning(u'Timeout reached!')
                    break

                self.logger.info(u'Performing template matching...')

                last_datetime = datetime.now()

                image = Image.open(self.default_path + image_path)
                image = image.convert(u'RGB')

                screenshot = self.take_screenshot()

                x_pos, y_pos = template_match(screenshot, image)

                self.logger.info(u'CLICK AT (%s, %s)', x_pos, y_pos)

                self.mouse.move(x_pos, y_pos)
                self.mouse.click(x_pos, y_pos)

                return

            except pykuli_exceptions.NoMatchException:
                self.logger.error(u'No match found, trying again...')

        self.logger.error(u'No match found, exiting!')


if __name__ == u'__main__':
    pykuli = Pykuli(u'../')
    pykuli.click(u'teste2.png', 10)
