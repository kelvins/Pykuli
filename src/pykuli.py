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

    MOUSE_BUTTON_MAPPING = {
        u'left': 1,
        u'right': 2,
        u'middle': 3,
    }

    def __init__(self, default_path=u'./', threshold=0.90):

        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        self.threshold = threshold
        self.default_path = default_path

        self.logger = logging.getLogger()

    def __keyboard_wrapper(self, method, param, prefix_msg):
        """
        Wrapper for the PyKeyboard methods.

        Args:
            method: PyKeyboard method.
            param: parameter passed to the PyKeyboard method.
            prefix_msg (unicode): prefix message which is shown in the logger.
        """
        self.logger.info(u'%s "%s"', prefix_msg, str(param))
        method(param)

    def press_key(self, key):
        """
        Wrapper for the PyKeyboard press_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.__keyboard_wrapper(self.keyboard.press_key, key, u'PRESS KEY')

    def release_key(self, key):
        """
        Wrapper for the PyKeyboard release_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.__keyboard_wrapper(self.keyboard.release_key, key, u'RELEASE KEY')

    def tap_key(self, key):
        """
        Wrapper for the PyKeyboard tap_key method.
        It is only used to show a logging for debugging purposes.
        """
        self.__keyboard_wrapper(self.keyboard.tap_key, key, u'TAP KEY')

    def type_string(self, keys):
        """
        Wrapper for the PyKeyboard type_string method.
        It is only used to show a logging for debugging purposes.
        """
        self.__keyboard_wrapper(self.keyboard.type_string, keys, u'TYPE STRING')

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
            image_path (unicode): path to the template image we want to match.

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
            image_path (unicode): path to the template image we want to match.
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

    def click(self, image_path, seconds=0, button=u'left'):
        """
        The click method is responsible for searching for a match
        and click on the object.

        Args:
            image_path (unicode): path to the template image we want to match.
            seconds (int): seconds to wait for the image to appear.
            button (unicode): mouse button option (e.g. left, right or middle).

        Raises:
            Raises the NoMatchFoundException exception if no match was found.
            Raises the InvalidMouseButtonException if the button is invalid.
        """

        # Check if the button option is valid before the template match
        if button not in self.MOUSE_BUTTON_MAPPING:
            raise pykuli_exceptions.InvalidMouseButtonException(
                u'Button "{}" is not a valid mouse button option'.format(button)
            )

        try:
            position = self.wait(image_path, seconds)
        except pykuli_exceptions.TimeoutException:
            raise pykuli_exceptions.NoMatchFoundException(
                u'No match was found using the "{image_path}" template with '
                u'a threshold of {threshold} in {seconds} second(s)'.format(
                    image_path=image_path,
                    threshold=self.threshold,
                    seconds=seconds
                )
            )

        x_pos, y_pos = position

        self.logger.info(u'CLICK AT %s', position)

        self.mouse.move(x_pos, y_pos)
        self.mouse.click(x_pos, y_pos, self.MOUSE_BUTTON_MAPPING[button])


if __name__ == u'__main__':
    pykuli = Pykuli(u'../img/')
    pykuli.click(u'teste.png')
    pykuli.type_string(u'a')
    pykuli.tap_key(u'return')
