#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pykuli_exceptions


def template_match(screenshot, image):

    screenshot_width = screenshot.size[0]
    screenshot_height = screenshot.size[1]

    image_width = image.size[0]
    image_height = image.size[1]

    # Get the pixel map of the two images
    screenshot_pm = screenshot.load()
    image_pm = image.load()

    for i1 in xrange(screenshot_width-image_width):
        for j1 in xrange(screenshot_height-image_height):

            try:
                for i2 in xrange(image_width):
                    for j2 in xrange(image_height):

                        if screenshot_pm[i1 + i2, j1 + j2] != image_pm[i2, j2]:
                            raise Exception(u'Pixel is not equal')

                return i1, j1# + (image_width / 2), j1 + (image_height / 2)

            except Exception:
                continue

    raise pykuli_exceptions.NoMatchException(u'There is no match')
