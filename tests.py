import unittest


class AnalysisInternal(unittest.TestCase):
    def test_group_reply(self):
        self.assertEqual(True, False)

    def test_group_retweet(self):
        self.assertEqual(True, False)

    def test_group_tweet(self):
        self.assertEqual(True, False)


class AnalysisExternal(unittest.TestCase):
    def test_analyse_type_small(self):
        self.assertEqual(True, False)


analysis_tests = [AnalysisInternal, AnalysisExternal]
analysis = unittest.TestSuite(map(unittest.TestLoader().loadTestsFromTestCase,
                                  analysis_tests))

ALL_TESTS = unittest.TestSuite([analysis])


def load_tests(loader=None, tests=None, pattern=None):
    return ALL_TESTS

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(ALL_TESTS)
