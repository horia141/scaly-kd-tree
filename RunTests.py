#!/usr/bin/env python

import unittest

import ScalyKDTreeTest

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromModule(ScalyKDTreeTest))
