# SymbolicEqual
Evaluates the equality between two symbolic expressions using the python [`SymPy`](https://docs.sympy.org/latest/index.html) package. 

Note that `pi` is a reserved constant and cannot be used as a symbol name.

This function allows omitting `*` and using `^` instead of `**` if the grading parameter `strict_syntax` is set to false. In this case it is also recommended to list any multicharacter symbols (that are not part of the default list of SI units) expected to appear in the response as input symbols.

## Inputs

### Optional grading parameters
If you want to use `I` for the imaginary constant, set the grading parameter `complexNumbers` to True.

If you want to use the special functions `beta` (Euler Beta function), `gamma` (Gamma function) and `zeta` (Riemann Zeta function), set the grading parameter `specialFunctions` to True.

## Outputs
Outputs to the `eval` command will feature:

```json
{
  "command": "eval",
  "result": {
    "is_correct": "<bool>",
    "response_latex": "<str>",
    "response_simplified": "<str>",
    "level": "<int>"
  }
}

```

### `response_latex`
This is a latex string, indicating how the user's `response` was understood by SymPy. It can be used to provide feedback in the front-end.

### `level`
The function tests equality using three levels, of increasing complexity. This parameter indicates the level at which equality was found. It is not present if the result is incorrect.

### `response_simplified`
This is a math-simplified string of the given response. All mathematically-equivalent expressions will yield identical strings under this field. This can be used by teacher dashboards when aggregating common student errors. 

## Examples
