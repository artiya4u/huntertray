import unittest
from huntertray import ProductHunt


class HNTest(unittest.TestCase):
    def runTest(self):
        data = ProductHunt.getHomePage()
        self.assertTrue(len(data) > 0)


if __name__ == '__main__':
    unittest.main()
