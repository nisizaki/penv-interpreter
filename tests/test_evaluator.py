import pytest

from penv import (
    App,
    BoolConst,
    BoolValue,
    Comp,
    Equal,
    Ext,
    Id,
    If,
    Lam,
    NameConst,
    NameValue,
    UnboundName,
    Var,
    empty_env,
    eval,
    lookup,
    update,
)


def reifier():
    return Lam("x", Lam("y", Id()))


def test_update_and_lookup_shadow_parent():
    env = update(empty_env(), "x", NameValue("old"))
    env = update(env, "x", NameValue("new"))

    assert lookup(env, "x") == NameValue("new")
    with pytest.raises(UnboundName):
        lookup(env, "missing")


def test_environment_reification_returns_environment_binding_arguments():
    term = App(App(reifier(), NameConst("m")), NameConst("n"))

    env = eval(term)

    assert lookup(env, "x") == NameValue("m")
    assert lookup(env, "y") == NameValue("n")


def test_environment_reflection_evaluates_term_under_reified_environment():
    identity = Lam("z", Var("z"))
    arg = NameConst("payload")
    reflected = Comp(App(Var("x"), Var("y")), App(App(reifier(), identity), arg))

    assert eval(reflected) == NameValue("payload")


def test_programmable_environment_closure_can_drive_variable_lookup():
    m = NameConst("m")
    n = NameConst("n")
    programmable_env = Lam(
        "i",
        If(
            Equal(Var("i"), NameConst("x")),
            m,
            n,
        ),
    )

    assert eval(Comp(Var("x"), programmable_env)) == NameValue("m")


def test_environment_as_function_applies_to_name_value():
    term = App(Ext(NameConst("m"), "x", Id()), NameConst("x"))

    assert eval(term) == NameValue("m")


def test_boolean_condition_and_equality():
    term = If(Equal(BoolConst(True), BoolConst(False)), NameConst("bad"), NameConst("ok"))

    assert eval(term) == NameValue("ok")
    assert eval(Equal(NameConst("x"), NameConst("x"))) == BoolValue(True)
