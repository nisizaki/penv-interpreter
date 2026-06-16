import pytest

from penv import (
    App,
    BoolConst,
    Comp,
    Equal,
    Ext,
    Id,
    If,
    Lam,
    NameConst,
    NameValue,
    ParseError,
    Var,
    eval,
    parse,
)


def test_parse_atoms():
    assert parse("x") == Var("x")
    assert parse('"x"') == NameConst("x")
    assert parse("id") == Id()
    assert parse("true") == BoolConst(True)
    assert parse("false") == BoolConst(False)


def test_parse_lambda_and_application():
    assert parse("lambda x. x") == Lam("x", Var("x"))
    assert parse("\\x. x") == Lam("x", Var("x"))
    assert parse("f x y") == App(App(Var("f"), Var("x")), Var("y"))


def test_parse_environment_extension_and_composition():
    assert parse('("m"/x).id') == Ext(NameConst("m"), "x", Id())
    assert parse("x circ ((lambda x. id) y)") == Comp(
        Var("x"),
        App(Lam("x", Id()), Var("y")),
    )


def test_parse_if_and_equal():
    assert parse('if i = "x" then "m" else "n"') == If(
        Equal(Var("i"), NameConst("x")),
        NameConst("m"),
        NameConst("n"),
    )


def test_parsed_environment_as_function_evaluates_with_existing_evaluator():
    term = parse('(("m"/x).id) "x"')

    assert eval(term) == NameValue("m")


def test_parse_rejects_trailing_input_and_unterminated_strings():
    with pytest.raises(ParseError):
        parse("lambda . x")
    with pytest.raises(ParseError):
        parse('"x')
