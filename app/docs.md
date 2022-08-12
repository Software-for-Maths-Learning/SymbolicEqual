# SymbolicEqual
Evaluates the equality between two symbolic expressions using the python [`SymPy`](https://docs.sympy.org/latest/index.html) package. 

Note that `pi` is a reserved constant and cannot be used as a symbol name.

The $\pm$ and $\mp$ symbols can be represented with `plus_minus` and `minus_plus` respectively. Since adding $\pm$ or $\mp$ turns creates two possible interpretations the criteria for equality. The default setting is that for each possible answer there must be a corresponding response and vice versa. It is also possible to only require that all responses are valid answers or that all answers can be found among the responses.

## Inputs

### Optional grading parameters
To use `I` for the imaginary constant, set the grading parameter `complexNumbers` to True.

To use the special functions `beta` (Euler Beta function), `gamma` (Gamma function) and `zeta` (Riemann Zeta function), set the grading parameter `specialFunctions` to True.

To use other symbols for $\pm$ and $\mp$ set the grading parameters `plus_minus` and `minus_plus` to te desired symbol. **Remark:** symbol replacement is brittle and can have unintended consequences.

Answers or responses that contain $\pm$ or $\mp$ has two possible interpretations which requires further criteria for equality. The grading parameter `multiple_answers_criteria` controls this. The default setting, `all`, is that each answer must have a corresponding answer and vice versa. The setting `all_responses` check that all responses are valid answers and the setting `all_answers` checks that all answers are found among the responses.

## Outputs
Outputs to the `eval` command will feature:

```json
{
  "command": "eval",
  "result": {
    "is_correct": "<bool>",
    "response_latex": "<str>"
  }
}

```

### `response_latex`
This is a latex string, indicating how the user's `response` was understood by SymPy. It can be used to provide feedback in the front-end.

## Examples
