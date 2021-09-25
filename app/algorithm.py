def grading_function(body: dict) -> dict:
    """
    Function used to grade a student response.
    ---
    The handler function passes only one argument to grading_function(),
    which is a dictionary of the structure of the API request body
    deserialised from JSON.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. This is also subject to
    standard response specifications.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that grading_function() is the main function used
    to output the grading response.
    """

    from sympy.parsing.sympy_parser import parse_expr
    from sympy import expand, simplify, trigsimp, latex

    # Safely try to parse answer and response into symbolic expressions
    try:
        res = parse_expr(body["response"])
    except SyntaxError as e:
        return {
            "error": {
                "type": "SyntaxError",
                "culprit": "user",
                "description": "SymPy was unable to parse your response",
                "dump": repr(e),
            }
        }
    except TypeError as e:
        return {
            "error": {
                "type": "TypeError",
                "culprit": "user",
                "description": "SymPy was unable to parse your response",
                "dump": repr(e),
            }
        }

    try:
        ans = parse_expr(body["answer"])
    except SyntaxError as e:
        return {
            "error": {
                "type": "SyntaxError",
                "culprit": "author",
                "decription":
                "Unable to parse answer field - SHEET DATA NEEDS TO BE CHANGED",
                "dump": repr(e),
            }
        }
    except TypeError as e:
        return {
            "error": {
                "type": "TypeError",
                "culprit": "author",
                "description":
                "Unable to parse answer field - SHEET DATA NEEDS TO BE CHANGED",
                "dump": repr(e),
            }
        }

    # Add how res was interpreted to the response
    interp = {"response_latex": latex(res)}

    # Going from the simplest to complex tranformations available in sympy, check equality
    # https://github.com/sympy/sympy/wiki/Faq#why-does-sympy-say-that-two-equal-expressions-are-unequal
    is_correct = bool(res.expand() == ans.expand())
    if is_correct:
        return {"is_correct": True, "level": "1", **interp}

    is_correct = bool(res.simplify() == ans.simplify())
    if is_correct:
        return {"is_correct": True, "level": "2", **interp}

    # Looks for trig identities
    is_correct = bool(res.trigsimp() == ans.trigsimp())
    if is_correct:
        return {"is_correct": True, "level": "3", **interp}

    return {"is_correct": False, **interp}
