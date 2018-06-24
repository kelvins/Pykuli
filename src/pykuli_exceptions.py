#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class PykuliBaseException(Exception):
    pass


class NoMatchFoundException(PykuliBaseException):
    pass


class TimeoutException(PykuliBaseException):
    pass


class InvalidMouseButtonException(PykuliBaseException):
    pass
