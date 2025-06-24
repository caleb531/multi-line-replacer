#!/usr/bin/env python3


import types
import unittest

import mlr


class TestMLR(unittest.TestCase):
    def test_module(self):
        self.assertIsInstance(mlr, types.ModuleType)
