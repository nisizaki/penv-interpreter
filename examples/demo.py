from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from penv import (  # noqa: E402
    App,
    BoolValue,
    Closure,
    Comp,
    EnvValue,
    Equal,
    Ext,
    Id,
    If,
    Lam,
    NameConst,
    NameValue,
    Var,
    eval,
    lookup,
)


def reifier() -> Lam:
    return Lam("x", Lam("y", Id()))


def describe(value: object) -> str:
    if isinstance(value, NameValue):
        return f'"{value.name}"'
    if isinstance(value, BoolValue):
        return "true" if value.value else "false"
    if isinstance(value, Closure):
        return f"<closure lambda {value.param}. ...>"
    if isinstance(value, EnvValue):
        bindings = []
        for name in ("x", "y"):
            try:
                bindings.append(f"{name}={describe(lookup(value, name))}")
            except Exception:
                pass
        suffix = f" {', '.join(bindings)}" if bindings else ""
        return f"<environment{suffix}>"
    return repr(value)


def print_result(title: str, value: object) -> None:
    print(f"{title}: {describe(value)}")


def main() -> None:
    identity = Lam("z", Var("z"))
    payload = NameConst("payload")

    env_reification = App(App(reifier(), identity), payload)
    reified_env = eval(env_reification)
    print_result("environment reification", reified_env)
    print(f"  lookup x -> {describe(lookup(reified_env, 'x'))}")
    print(f"  lookup y -> {describe(lookup(reified_env, 'y'))}")

    env_reflection = Comp(App(Var("x"), Var("y")), env_reification)
    print_result("environment reflection", eval(env_reflection))

    programmable_env = Lam(
        "i",
        If(
            Equal(Var("i"), NameConst("x")),
            NameConst("matched-x"),
            NameConst("fallback"),
        ),
    )
    print_result("programmable environment", eval(Comp(Var("x"), programmable_env)))

    env_as_function = App(Ext(NameConst("stored"), "x", Id()), NameConst("x"))
    print_result("environment as function", eval(env_as_function))


if __name__ == "__main__":
    main()
