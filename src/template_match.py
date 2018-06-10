#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pykuli_exceptions


def template_match(screenshot, image):
    """
    This function is used to perform template matching
    between the screenshot and the image we want to find.
    It will look pixel by pixel.

    Args:
        screenshot (pillow image): screenshot from the 1st monitor.
        image (pillow image): image we want to search.

    Return:
        Return a tuple with the positions (e.g. (x, y)) of the
        center of the image that matches, so we can click on it.

    Raises:
        If could not find any match it will raises the
        pykuli_exceptions.NoMatchException.
    """

    screenshot_width = screenshot.size[0]
    screenshot_height = screenshot.size[1]

    image_width = image.size[0]
    image_height = image.size[1]

    # Get the pixel map of the two images
    screenshot_pm = screenshot.load()
    image_pm = image.load()

    # For each row, go through each column
    for y1 in xrange(screenshot_height-image_height):
        for x1 in xrange(screenshot_width-image_width):

            try:
                # For each row, go through each column
                for y2 in xrange(image_height):
                    for x2 in xrange(image_width):

                        if screenshot_pm[x1 + x2, y1 + y2] != image_pm[x2, y2]:
                            raise Exception(u'Pixel is not equal')

                return (
                    x1 + (image_width / 2),
                    y1 + (image_height / 2)
                )

            except Exception:
                continue

    raise pykuli_exceptions.NoMatchException(u'There is no match')
