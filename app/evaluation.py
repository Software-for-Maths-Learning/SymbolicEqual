def evaluation_function(response, answer, params) -> dict:
    """
    Function used to grade a student response.
    ---
    The handler function passes only one argument to evaluation_function(),
    which is a dictionary of the structure of the API request body
    deserialised from JSON.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. This is also subject to
    standard response specifications.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the grading response.
    """

    from sympy.parsing.sympy_parser import parse_expr
    from sympy import expand, simplify, trigsimp, latex

    # Safely try to parse answer and response into symbolic expressions
    try:
        res = parse_expr(response)
    except (SyntaxError, TypeError) as e:
        raise Exception("SymPy was unable to parse the response") from e

    try:
        ans = parse_expr(answer)
    except (SyntaxError, TypeError) as e:
        raise Exception("SymPy was unable to parse the answer") from e

    # Add how res was interpreted to the response
    interp = {"response_latex": latex(res)}
    
    # Dealing with special cases
    res, ans = RecpTrig(res, ans)

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

def RecpTrig(res, ans):
    """
    Reciprocal Trig Functions -> Turn sec, csc, cot into sin form
    
    Parameters
    ----------
    res : SymPy expression
        Reponse Input from Teacher, might have sec, csc, cot
    ans : SymPy expression
        Answer Input from Student, might have sec, csc, cot

    Returns
    -------
    res : SymPy expression
        Updated response input
    ans : SymPy expression
        Updated answer input
    """
    from sympy import sec, csc, cot, sin
    if res.has(sec) or res.has(csc) or res.has(cot):
        res = res.rewrite(sin)
    if ans.has(sec) or ans.has(csc) or ans.has(cot):
        ans = ans.rewrite(sin)
    return res, ans

