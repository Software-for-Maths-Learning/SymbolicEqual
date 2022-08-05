import unittest

try:
    from .evaluation import evaluation_function
except ImportError:
    from evaluation import evaluation_function

class TestEvaluationFunction(unittest.TestCase):
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

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_simple_polynomial_correct(self):
        body = {"response": "3*x**2 + 3*x +  5", "answer": "2+3+x+2*x + x*x*3"}

        response = evaluation_function(body['response'], body['answer'], {})

        self.assertEqual(response.get("is_correct"), True)

    def test_simple_polynomial_incorrect(self):
        body = {
            "response": "3*x**2 + 3*x +  5",
            "answer": "2+3+x+2*x + x*x*3 - x"
        }

        response = evaluation_function(body['response'], body['answer'], {})

        self.assertEqual(response.get("is_correct"), False)

    def test_simple_trig_correct(self):
        body = {"response": "cos(x)**2 + sin(x)**2 + y", "answer": "y + 1"}

        response = evaluation_function(body['response'], body['answer'], {})

        self.assertEqual(response.get("is_correct"), True)

    def test_invalid_user_expression(self):
        body = {"response": "3x", "answer": "3*x"}

        self.assertRaises(
            Exception,
            evaluation_function,
            body["response"],
            body["answer"],
            {},
        )

    def test_invalid_author_expression(self):
        body = {"response": "3*x", "answer": "3x"}

        self.assertRaises(
            Exception,
            evaluation_function,
            body["response"],
            body["answer"],
            {},
        )

    def test_recp_trig_correct(self):
        body = {"response": "1+tan(x)**2 + y", "answer": "sec(x)**2 + y"}

        response = evaluation_function(body['response'], body['answer'], {})

        self.assertEqual(response.get("is_correct"), True)

    def test_decimals_correct(self):
        body = {"response": "x/2", "answer": "x*0.5"}
        
        response = evaluation_function(body['response'], body['answer'], {})

        self.assertEqual(response.get("is_correct"), True)

    def test_absolute_correct(self):
        body = {"response": "|x|+y", "answer": "Abs(x)+y"}

        response = evaluation_function(body['response'], body['answer'], {})

        self.assertEqual(response.get("is_correct"), True)

    def test_nested_absolute_error(self):
        body = {"response": "|x+|y||", "answer": "Abs(x+Abs(y))"}

        with self.assertRaises(SyntaxWarning) as cm:
            evaluation_function(body["response"], body["answer"], {})

        self.assertEqual(cm.exception.args[1] == "tooMany|InResponse", True)

    def test_many_absolute_error(self):
        body = {"response": "Abs(x)+Abs(y)", "answer": "|x|+|y|"}

        with self.assertRaises(SyntaxWarning) as cm:
            evaluation_function(body["response"], body["answer"], {})

        self.assertEqual(cm.exception.args[1] == "tooMany|InAnswer", True)

    def test_clashing_symbols(self):
        params = {}
        response = "beta+gamma+zeta+I+N+O+Q+S+E"
        answer = "E+S+Q+O+N+I+zeta+gamma+beta"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result.get("is_correct"), True)

    def test_special_constants(self):
        response = "pi"
        answer = "2*asin(1)"
        params = {}
        result = evaluation_function(response, answer, params)
        self.assertEqual(result.get("is_correct"), True)

    def test_complex_numbers(self):
        response = "I"
        answer = "(-1)**(1/2)"
        params = {"complexNumbers": True}
        result = evaluation_function(response, answer, params)
        self.assertEqual(result.get("is_correct"), True)

    def test_special_functions(self):
        params = {"specialFunctions": True}
        response = "beta(1,x)"
        answer = "1/x"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result.get("is_correct"), True)
        response = "gamma(5)"
        answer = "4*3*2"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result.get("is_correct"), True)
        response = "zeta(2)"
        answer = "pi**2/6"
        result = evaluation_function(response, answer, params)
        self.assertEqual(result.get("is_correct"), True)

if __name__ == "__main__":
    unittest.main()
