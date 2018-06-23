#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The Pykuli project is inspired by Sikuli.
With the Pykuli class you can automate everything you see.
"""
import os
import logging
from logging.config import fileConfig
from datetime import datetime, timedelta

from mss import mss
from skimage import io
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

    def __init__(self, default_path=u'./'):

        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        self.default_path = default_path

        self.logger = logging.getLogger()

    def press_key(self, key):
        """
        Wrapper for the PyKeyboard press_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'PRESS KEY "%s"', str(key))
        self.keyboard.press_key(key)

    def release_key(self, key):
        """
        Wrapper for the PyKeyboard release_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'RELEASE KEY "%s"', str(key))
        self.keyboard.release_key(key)

    def tap_key(self, key):
        """
        Wrapper for the PyKeyboard tap_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'TAP KEY "%s"', str(key))
        self.keyboard.tap_key(key)

    def type_string(self, string):
        """
        Wrapper for the PyKeyboard type_string method.
        It is only used to show a logging for debugging purposes.
        """
        self.logger.info(u'TYPE STRING "%s"', string)
        self.keyboard.type_string(string)

    def take_screenshot(self):
        """
        This method uses the mss package to take a screen shot of the screen.

        Returns:
            Return the screenshot (grayscale) as an scikit image object.
        """
        with mss() as sct:
            file_name = sct.shot()

        screenshot = io.imread(file_name, as_gray=True)

        os.remove(file_name)

        return screenshot

    def exists(self, image_path):
        """
        Check if a template matching exists.

        Args:
            image_path (str): path to the image we want to match.

        Return:
            If the image exists, it will return a tuple with the
            position (e.g. (x, y)), otherwise it will return None.
        """
        try:
            image = io.imread(self.default_path + image_path, as_gray=True)

            screenshot = self.take_screenshot()

            return template_match(screenshot, image)

        except pykuli_exceptions.NoMatchException:
            return None

    def wait(self, image_path, seconds=0):
        """
        Wait for an element to appear at most N seconds.

        Args:
            image_path (str): path to the image we want to match.
            Note that this will be concatenated to the default_path.
            seconds (int): seconds to wait for the image to appear.
        """

        datetime_limit = datetime.now() + timedelta(seconds=seconds)
        last_datetime = None

        # Load the template image in grayscale
        image = io.imread(self.default_path + image_path, as_gray=True)

        while True:

            if last_datetime and last_datetime > datetime_limit:
                self.logger.warning(u'Timeout reached!')
                break

            last_datetime = datetime.now()

            screenshot = self.take_screenshot()

            try:
                return template_match(screenshot, image)
            except pykuli_exceptions.NoMatchException:
                continue

        return None

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

        self.logger.info(u'Performing template matching...')

        position = self.wait(image_path, seconds)

        if not position:
            self.logger.error(u'No match found, exiting!')
            return

        x_pos, y_pos = position

        self.logger.info(u'CLICK AT %s', position)

        self.mouse.move(x_pos, y_pos)
        self.mouse.click(x_pos, y_pos)


if __name__ == u'__main__':
    pykuli = Pykuli(u'../img/')
    pykuli.click(u'teste.png')
    pykuli.type_string(u'a')
    pykuli.tap_key('return')
