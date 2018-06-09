#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time


class Pykuli(object):

    def __init__(self, default_path=u''):
        self.default_path = default_path

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)
