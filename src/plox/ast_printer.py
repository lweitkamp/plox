from functools import singledispatch

from plox.expressions import Binary, Grouping, Literal, Unary


@singledispatch
def pretty_print(expr):
    raise TypeError


@pretty_print.register
def _(expr: Literal):
    return "nil" if expr.value is None else str(expr.value)


@pretty_print.register
def _(expr: Binary):
    return f"{pretty_print(expr.left)} {expr.operator.lexeme} {pretty_print(expr.right)}"


@pretty_print.register
def _(expr: Grouping):
    return f"({pretty_print(expr.expression)})"


@pretty_print.register
def _(expr: Unary):
    return f"({expr.operator.lexeme} {pretty_print(expr.right)})"
