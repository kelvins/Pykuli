#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
from skimage.feature import match_template

import pykuli_exceptions


def template_match(screenshot, image):
    """
    Perform the template match and return the X and Y positions
    when there is a valid match.

    Args:
        screenshot (scikit image): screenshot image.
        image (scikit image): template image.

    Returns:
        Return the X and Y positions if there is a match.

    Raises:
        Raises de NoMatchException exception if there is no match.
    """

    result = match_template(screenshot, image, pad_input=True)

    x, y = np.unravel_index(np.argmax(result), result.shape)[::-1]

    return (
        x / 2,
        y / 2
    )

    raise pykuli_exceptions.NoMatchException(u'There is no match')
