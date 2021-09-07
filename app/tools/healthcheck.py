import unittest, time

"""
    Extension of the default TestResult class with timing information.
"""

class HealthcheckResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_timings = []

    def startTest(self, test):
        self._start_time = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed_time_s = time.time() - self._start_time
        elapsed_time_us = round(1000000 * elapsed_time_s)
        self.test_timings.append((test.id(), elapsed_time_us))

        super().addSuccess(test)

    def getTestTimings(self):
        return self.test_timings

"""
    Extension of the default TestRunner class that returns a JSON-encodable result
"""

class HealthcheckRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        return super().__init__(resultclass=HealthcheckResult, *args, **kwargs)
    
    def run(self, test):
        result = super().run(test)

        results = {
            "tests_passed": result.wasSuccessful(),
            "successes": [{"name": n, "time": t} for (n, t) in result.getTestTimings()], 
            "failures": [{"name": i.id(), "traceback": tb} for (i, tb) in result.failures], 
            "errors": [{"name": i.id(), "traceback": tb} for (i, tb) in result.errors]
        }

        return results