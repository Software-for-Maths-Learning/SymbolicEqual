from typing import Dict, List, TypedDict

import sympy
from latex2sympy2 import latex2sympy
from sympy.parsing import parse_expr
from sympy.printing.latex import LatexPrinter
from typing_extensions import NotRequired

from .evaluation import evaluation_function
from .expression_utilities import extract_latex, SymbolDict

class Params(TypedDict):
    is_latex: bool
    simplify: NotRequired[bool]
    symbols: NotRequired[SymbolDict]


class Preview(TypedDict):
    latex: str
    sympy: str


class Result(TypedDict):
    preview: Preview


def parse_latex(response: str, symbols: SymbolDict) -> str:
    """Parse a LaTeX string to a sympy string while preserving custom symbols.

    Args:
        response (str): The LaTeX expression to parse.
        symbols (SymbolDict): A mapping of sympy symbol strings and LaTeX
        symbol strings.

    Raises:
        ValueError: If the LaTeX string or symbol couldn't be parsed.

    Returns:
        str: The expression in sympy syntax.
    """
    substitutions = {}

    for sympy_symbol_str in symbols:
        symbol_str = symbols[sympy_symbol_str]["latex"]
        latex_symbol_str = extract_latex(symbol_str)

        try:
            latex_symbol = latex2sympy(latex_symbol_str)
        except Exception:
            raise ValueError(
                f"Couldn't parse latex symbol {latex_symbol_str} "
                f"to sympy symbol."
            )

        substitutions[latex_symbol] = sympy.Symbol(sympy_symbol_str)

    try:
        expression = latex2sympy(response, substitutions)

        if isinstance(expression, list):
            expression = expression.pop()

        return str(expression.xreplace(substitutions))  # type: ignore

    except Exception as e:
        raise ValueError(str(e))


def preview_function(response: str, params: Params) -> Result:
    """
    Function used to preview a student response.
    ---
    The handler function passes three arguments to preview_function():

    - `response` which are the answers provided by the student.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you.
    """
    symbols: SymbolDict = params.get("symbols", {})

    if not response:
        return Result(preview=Preview(latex="", sympy=""))

    try:
        if params.get("is_latex", False):
            response = parse_latex(response, symbols)

#        equation = parse_expr(
#            response,
#            evaluate=False,
#            local_dict=sympy_symbols(symbols),
#            transformations="all",
#        )

#        if params.get("simplify", False):
#            equation = sympy.simplify(equation)
#
#        latex_out = LatexPrinter(
#            {"symbol_names": latex_symbols(symbols)}
#        ).doprint(equation)

#        sympy_out = str(equation)

        try:
            result = evaluation_function(response, response, params)
        except Exception as e:
            raise ValueError("Failed to parse Sympy expression") from e

        latex_out = result["response_latex"]
        sympy_out = result["response_simplified"]

        if latex_out == "":
            raise ValueError("Evaluation function did not return LaTeX for response")
        if sympy_out == "":
            raise SyntaxError("Evaluation function did not return sympy for response")

    except SyntaxError as e:
        raise ValueError("Failed to parse Sympy expression") from e
    except ValueError as e:
        raise ValueError("Failed to parse LaTeX expression") from e
#    except Exception as e:
#        raise ValueError("Failed to generate preview") from e

    return Result(preview=Preview(latex=latex_out, sympy=sympy_out))
