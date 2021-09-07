import json, unittest, sys, os

from typing import Tuple

from ..algorithm import grading_function
from ..tests import TestSchemaValidation, TestGradingFunction

from .validate import validate_request
from .healthcheck import HealthcheckRunner

"""
    Healthcheck Methods
"""

def healthcheck() -> dict:
    """
    Function used to return the results of the unittests in a JSON-encodable format.
    ---
    Therefore, this can be used as a healthcheck to make sure the algorithm is 
    running as expected, and isn't taking too long to complete due to, e.g., issues 
    with load balancing.
    """

    # Redirect stderr stream to a null stream so the unittests are not logged on the console.
    no_stream = open(os.devnull, 'w')
    sys.stderr = no_stream

    # Create a test loader and test runner instance
    loader = unittest.TestLoader()

    schema_tests = loader.loadTestsFromTestCase(TestSchemaValidation)
    grading_tests = loader.loadTestsFromTestCase(TestGradingFunction)

    suite = unittest.TestSuite([schema_tests, grading_tests])
    runner = HealthcheckRunner(verbosity=0)

    result = runner.run(suite)

    # Reset stderr and close the null stream
    sys.stderr = sys.__stderr__
    no_stream.close()

    return result

"""
    Parsing Methods
"""

def load_body(body_text: str) -> Tuple[dict, dict]:
    """
    Function to convert JSON-encoded string of the request body into a dictionary.
    ---
    Returns a tuple, first element of which is the body, second of which is a 
    JSON-encodable dictionary containing errors and helpful messages which can be used
    as a response.

    If the body could not be loaded, an empty dictionary is returned.
    """

    body, errors = dict(), dict()

    # Attempt to load the body text
    try:
        body = json.loads(body_text)
    # Catch Decode errors and return the problems back to the requester.
    except json.JSONDecodeError as e:
            errors["message"] = "JSONDecodeError: Request body is not valid JSON."
            errors["error"] = {
                "message": e.msg,
                "location": {
                    "line": e.lineno,
                    "column": e.colno
                }
            }
    # Catch type error problems incase the body is not a string (for testing purposes).
    except TypeError:
        errors["message"] = "TypeError: Request body is not decoded JSON."

    return (body, errors)

def parse_body(event: dict) -> Tuple[dict, dict]:
    """
    Function to parse the request body into a dictionary from an AWS Event object.
    ---
    Returns a tuple, first element of which is the body, second of which is a 
    JSON-encodable dictionary containing errors and helpful messages which can be used
    as a response.

    If the body could not be loaded, an empty dictionary is returned.
    """

    body, response = dict(), dict()

    # Check if body exits in the event
    if "body" not in event:
        response = {
            "message": "LookupError: No grading data supplied in request body."
        }

        return (None, response)

    # If it does, convert the body into a dictionary.
    if type(event["body"]) == str:
        body, response = load_body(event["body"])
    else:
        body = event["body"]
    
    return (body, response)

"""
    Main Handler Method
"""

def handler(event, context={}):
    """
    Main function invoked by AWS Lambda to handle incoming grading requests.
    ---

    This function parses the body data from the event object, validates the information
    using a schema and returns the result from the grading function.

    If the parsing or validation fails at any point, the handler will return the issue
    back to the requester.
    """
    headers = event.get("headers", dict())
    command = headers.get("command", "grade")

    response = {"command": command}

    if command == "healthcheck":
        response["result"] = healthcheck()
        return response
    elif command != "grade":
        response["error"] = {"message": f"'{command}' is not a valid command."}
        return response

    body, parse_error = parse_body(event)

    if parse_error:
        response["error"] = parse_error
        return response
    
    validation_error = validate_request(body)

    if validation_error:
        response["error"] = validation_error
        return response

    response["result"] = grading_function(body)

    return response