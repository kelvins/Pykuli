#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
sys.path.append(u'.')
sys.path.append(u'..')

import pytest
from skimage import io

from src.pykuli import Pykuli
from src import pykuli_exceptions


class TestPykuli(object):

    def test_exists_with_valid_template(self):
        pykuli = Pykuli(u'tests/resources/')
        template_path = pykuli.default_path + u'template_test.png'

        # Extract and save a template from a screenshot
        template = pykuli.take_screenshot()
        template = template[0:100, 0:100]
        io.imsave(template_path, template)

        expected_result = (25, 25)
        result = pykuli.exists(u'template_test.png')

        # Remove the saved image file
        os.remove(template_path)

        assert result == expected_result

    def test_exists_with_invalid_template(self):
        pykuli = Pykuli(u'tests/resources/')
        with pytest.raises(pykuli_exceptions.NoMatchFoundException):
            pykuli.exists(u'pykuli.png')

    def test_wait_with_valid_template(self):
        pykuli = Pykuli(u'tests/resources/')
        template_path = pykuli.default_path + u'template_test.png'

        # Extract and save a template from a screenshot
        template = pykuli.take_screenshot()
        template = template[0:100, 0:100]
        io.imsave(template_path, template)

        expected_result = (25, 25)
        result = pykuli.wait(u'template_test.png')

        # Remove the saved image file
        os.remove(template_path)

        assert result == expected_result

    def test_wait_with_invalid_template(self):
        pykuli = Pykuli(u'tests/resources/')
        with pytest.raises(pykuli_exceptions.TimeoutException):
            pykuli.wait(u'pykuli.png')
