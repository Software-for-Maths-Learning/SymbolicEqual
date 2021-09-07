import unittest

from ..algorithm import grading_function


class TestGradingFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use grading_function() to check your algorithm works
    as it should.
    """

    def test_simple_polynomial_correct(self):
        body = {"response": "3*x**2 + 3*x +  5", "answer": "2+3+x+2*x + x*x*3"}

        response = grading_function(body)

        self.assertEqual(response.get("is_correct"), True)

    def test_simple_polynomial_incorrect(self):
        body = {"response": "3*x**2 + 3*x +  5", "answer": "2+3+x+2*x + x*x*3 - x"}

        response = grading_function(body)

        self.assertEqual(response.get("is_correct"), False)

    def test_simple_trig_correct(self):
        body = {"response": "cos(x)**2 + sin(x)**2 + y", "answer": "y + 1"}

        response = grading_function(body)

        self.assertEqual(response.get("is_correct"), True)

    def test_simple_trig_correct(self):
        body = {"response": "cos(x)**2 + sin(x)**2 + y", "answer": "y + 1"}

        response = grading_function(body)

        self.assertEqual(response.get("is_correct"), True)

    def test_invalid_user_expression(self):
        body = {"response": "3x", "answer": "3*x"}

        response = grading_function(body)

        self.assertEqual(response.get("error", {}).get("culprit"), "user")

    def test_invalid_author_expression(self):
        body = {"response": "3*x", "answer": "3x"}

        response = grading_function(body)

        self.assertEqual(response.get("error", {}).get("culprit"), "author")


if __name__ == "__main__":
    unittest.main()
