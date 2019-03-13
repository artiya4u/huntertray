import unittest
from huntertray import Version


class VersionTest(unittest.TestCase):
    def run_test(self):
        version = Version.latest()
        assert version


if __name__ == '__main__':
    unittest.main()
