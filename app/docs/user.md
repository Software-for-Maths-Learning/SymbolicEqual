# SymbolicEqual

This function utilises the [`SymPy`](https://docs.sympy.org/latest/index.html) to provide a maths-aware comparsion of a student's response to the correct answer. This means that mathematically equivalent inputs will be marked as correct. Note that `pi` is a reserved constant and cannot be used as a symbol name.

## Inputs

### Optional grading parameters

There are four optional parameters that can be set: `complexNumbers`, `specialFunctions`, `strict_syntax` and `symbol_assumptions`.

## `complexNumbers`

If you want to use `I` for the imaginary constant, set the grading parameter `complexNumbers` to True.

## `specialFunctions`

If you want to use the special functions `beta` (Euler Beta function), `gamma` (Gamma function) and `zeta` (Riemann Zeta function), set the grading parameter `specialFunctions` to True.

## `strict_syntax`

If `strict_syntax` is set to true then the answer and response must have `*` or `/` between each part of the expressions and exponentiation must be done using `**`, e.g. `10*x*y/z**2` is accepted but `10xy/z^2` is not.

If `strict_syntax` is set to false, then `*` can be omitted and `^` used instead of `**`. In this case it is also recommended to list any multicharacter symbols expected to appear in the response as input symbols.

By default `strict_syntax` is set to true.

## `symbol_assumptions`

This input parameter allows the author to set an extra assumption each symbol. Each assumption should be written on the form `('symbol','assumption name')` and all pairs concatenated into a single string.

The possible assumption names can be found in this list: 
[`SymPy Assumption Predicates`](https://docs.sympy.org/latest/guides/assumptions.html#predicates)

## Examples

Implemented versions of these examples can be found in the module 'Examples: Evaluation Functions'.

### 1 Setting input symbols to be assumed positive to avoid issues with fractional powers

In general $\frac{\sqrt{a}}{\sqrt{b}} \neq \sqrt{\frac{a}{b}}$ but if $a > 0$ and $b > 0$ then $\frac{\sqrt{a}}{\sqrt{b}} = \sqrt{\frac{a}{b}}$. The same is true for other fractional powers.

So if expression like these are expected in the answer and/or response then it is a good idea to use the `symbol_assumptions` parameter to note that $a > 0$ and $b > 0$. This can be done by setting `symbol_assumptions` to `('a','positive') ('b','positive')`.

The example given in the example problem set uses an EXPRESSION response area that uses `SymbolicEqual` with answer `sqrt(a/b)`, `strict_syntax` set to false and `symbol_assumptions` set as above. Some examples of expressions that are accepted as correct:
`sqrt(a)/sqrt(b)`, `(a/b)**(1/2)`, `a**(1/2)/b**(1/2)`, `(a/b)**(0.5)`, `a**(0.5)/b**(0.5)`