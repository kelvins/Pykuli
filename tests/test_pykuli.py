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

    @staticmethod
    def get_template_based_on_platform(template):
        if sys.platform == u'darwin':
            return template[0:100, 0:100]
        return template[0:20, 0:20]

    @staticmethod
    def get_expected_result_based_on_platform():
        if sys.platform == u'darwin':
            return 25, 25
        return 5, 5

    def test_exists_with_valid_template(self):
        pykuli = Pykuli(u'tests/resources/')
        template_path = pykuli.default_path + u'template_test.png'

        # Extract and save a template from a screenshot
        template = pykuli.take_screenshot()
        template = self.get_template_based_on_platform(template)
        io.imsave(template_path, template)

        expected_result = self.get_expected_result_based_on_platform()
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
        template = self.get_template_based_on_platform(template)
        io.imsave(template_path, template)

        expected_result = self.get_expected_result_based_on_platform()
        result = pykuli.wait(u'template_test.png')

        # Remove the saved image file
        os.remove(template_path)

        assert result == expected_result

    def test_wait_with_invalid_template(self):
        pykuli = Pykuli(u'tests/resources/')
        with pytest.raises(pykuli_exceptions.TimeoutException):
            pykuli.wait(u'pykuli.png')
