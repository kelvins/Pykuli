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
        This parameter will be used as a prefix for all methods that
        uses a template image.
        threshold (float): threshold used to consider a match.
    """

    def __init__(self, default_path=u'./', threshold=0.90):

        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        self.threshold = threshold
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

    @staticmethod
    def take_screenshot():
        """
        Static method which uses the mss package to take a
        screen shot and return it as a scikit image.

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
        Check if there is a match between the template image
        (path passed by parameter) and the current screen shot.

        Args:
            image_path (str): path to the template image we want to match.

        Return:
            If a match was found, it will return the X and Y positions (tuple).

        Raises:
            Raises the NoMatchFoundException exception if no match was found.
        """
        image = io.imread(self.default_path + image_path, as_gray=True)

        screenshot = self.take_screenshot()

        return template_match(screenshot, image, self.threshold)

    def wait(self, image_path, seconds=0):
        """
        Implicit wait. Wait for an element to appear at most N seconds.

        Args:
            image_path (str): path to the template image we want to match.
            seconds (int): seconds to wait for the image to appear.

        Returns:
            If a match was found, it will return the X and Y positions (tuple).

        Raises:
            Raises the TimeoutException exception if no match was found.
        """

        datetime_limit = datetime.now() + timedelta(seconds=seconds)
        last_datetime = None

        # Load the template image in grayscale
        image = io.imread(self.default_path + image_path, as_gray=True)

        while True:

            if last_datetime and last_datetime > datetime_limit:
                raise pykuli_exceptions.TimeoutException()

            last_datetime = datetime.now()

            screenshot = self.take_screenshot()

            try:
                return template_match(screenshot, image, self.threshold)
            except pykuli_exceptions.NoMatchFoundException:
                continue

    def click(self, image_path, seconds=0):
        """
        The click method is responsible for searching for a match
        and click on the object.

        Args:
            image_path (str): path to the template image we want to match.
            seconds (int): seconds to wait for the image to appear.

        Raises:
            Raises the NoMatchFoundException exception if no match was found.
        """

        self.logger.info(u'Performing template matching...')

        try:
            position = self.wait(image_path, seconds)
        except pykuli_exceptions.TimeoutException:
            raise pykuli_exceptions.NoMatchFoundException(
                u'No match was found using the {image_path} template with '
                u'a threshold of {threshold} in {seconds} second(s)'.format(
                    image_path=image_path,
                    threshold=self.threshold,
                    seconds=seconds
                )
            )

        x_pos, y_pos = position

        self.logger.info(u'CLICK AT %s', position)

        self.mouse.move(x_pos, y_pos)
        self.mouse.click(x_pos, y_pos)


if __name__ == u'__main__':
    pykuli = Pykuli(u'../img/')
    pykuli.click(u'teste.png')
    pykuli.type_string(u'a')
    pykuli.tap_key('return')
