import unittest

from ..tools.validate import validate_request

class TestSchemaValidation(unittest.TestCase):
    """
        TestCase Class used to test the schema.
        ---
        Tests are used here to check that the schema is able to 
        validate and reject request bodies that would otherwise 
        cause the program to crash.
        
        It's best practise to write these tests first to get a 
        kind of 'specification' for what your schema should 
        accept or reject, and you should run these tests before 
        committing your code to git.

        Read the docs on how to use unittest here:
        https://docs.python.org/3/library/unittest.html

        Use validate_request() to check your schema works as 
        it should.
    """
    def test_empty_request_body(self):
        body = {}

        validation_error = validate_request(body)

        self.assertNotEqual(validation_error, None)
        self.assertEqual(validation_error.get("message"), "Schema threw an error when validating the request body.")

    def test_invalid_grading_data(self):
        body = {"hello": "world"}

        validation_error = validate_request(body)

        self.assertNotEqual(validation_error, None)
        self.assertEqual(validation_error.get("message"), "Schema threw an error when validating the request body.")

    def test_valid_grading_data(self):
        body = {"example": "property"}

        validation_error = validate_request(body)

        self.assertEqual(validation_error, None)

if __name__ == "__main__":
    unittest.main()