from __future__ import annotations

from penv.ast import (
    App,
    BoolConst,
    Comp,
    Equal,
    Ext,
    Id,
    If,
    Lam,
    NameConst,
    Term,
    Var,
)
from penv.runtime import BoolValue, Closure, EnvValue, NameValue, TypeMismatch, Value


def empty_env() -> EnvValue:
    return EnvValue.empty()


def eval(term: Term, env: Value | None = None) -> Value:
    rho = empty_env() if env is None else env

    match term:
        case Var(name):
            return lookup(rho, name)
        case Lam(param, body):
            return Closure(param, body, rho)
        case App(fn, arg):
            return apply(eval(fn, rho), eval(arg, rho))
        case Id():
            return rho
        case Ext(value_term, var, env_term):
            return update(eval(env_term, rho), var, eval(value_term, rho))
        case Comp(inner, env_term):
            return eval(inner, eval(env_term, rho))
        case NameConst(name):
            return NameValue(name)
        case BoolConst(value):
            return BoolValue(value)
        case If(cond, then_branch, else_branch):
            condition = eval(cond, rho)
            if not isinstance(condition, BoolValue):
                raise TypeMismatch("if condition must evaluate to a boolean")
            branch = then_branch if condition.value else else_branch
            return eval(branch, rho)
        case Equal(left, right):
            return BoolValue(values_equal(eval(left, rho), eval(right, rho)))


def apply(fn: Value, arg: Value) -> Value:
    if isinstance(fn, Closure):
        return eval(fn.body, update(fn.env, fn.param, arg))
    if isinstance(fn, EnvValue):
        if not isinstance(arg, NameValue):
            raise TypeMismatch("environment application expects a name value")
        return fn.lookup(arg.name)
    raise TypeMismatch(f"value is not applicable: {fn!r}")


def lookup(env: Value, name: str) -> Value:
    if isinstance(env, EnvValue):
        return env.lookup(name)
    if isinstance(env, Closure):
        return apply(env, NameValue(name))
    raise TypeMismatch(f"value cannot be used as an environment: {env!r}")


def update(env: Value, name: str, value: Value) -> EnvValue:
    parent = env

    def lookup_updated(query: str) -> Value:
        if query == name:
            return value
        return lookup(parent, query)

    return EnvValue(lookup_updated)


def values_equal(left: Value, right: Value) -> bool:
    if isinstance(left, NameValue) and isinstance(right, NameValue):
        return left.name == right.name
    if isinstance(left, BoolValue) and isinstance(right, BoolValue):
        return left.value == right.value
    raise TypeMismatch("equality is currently defined for names and booleans")
