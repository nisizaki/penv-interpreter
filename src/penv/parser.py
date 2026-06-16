from __future__ import annotations

from dataclasses import dataclass

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


class ParseError(ValueError):
    pass


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int


KEYWORDS = {"lambda", "id", "true", "false", "if", "then", "else", "circ"}
SYMBOLS = set("()./=")


def parse(source: str) -> Term:
    parser = Parser(tokenize(source))
    return parser.parse()


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    while i < len(source):
        char = source[i]
        if char.isspace():
            i += 1
            continue
        if char in SYMBOLS:
            tokens.append(Token("symbol", char, i))
            i += 1
            continue
        if char == "\\":
            tokens.append(Token("keyword", "lambda", i))
            i += 1
            continue
        if char == '"':
            tokens.append(_read_string(source, i))
            i = tokens[-1].position + len(tokens[-1].value) + 2
            continue
        if char.isalpha() or char == "_":
            start = i
            i += 1
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
            value = source[start:i]
            kind = "keyword" if value in KEYWORDS else "ident"
            tokens.append(Token(kind, value, start))
            continue
        raise ParseError(f"unexpected character {char!r} at position {i}")
    tokens.append(Token("eof", "", len(source)))
    return tokens


def _read_string(source: str, start: int) -> Token:
    i = start + 1
    chars: list[str] = []
    while i < len(source):
        char = source[i]
        if char == '"':
            return Token("string", "".join(chars), start)
        if char == "\\":
            i += 1
            if i >= len(source):
                break
            char = source[i]
        chars.append(char)
        i += 1
    raise ParseError(f"unterminated string at position {start}")


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def parse(self) -> Term:
        term = self.parse_term(stop={"eof"})
        self.expect_kind("eof")
        return term

    def parse_term(self, stop: set[str]) -> Term:
        if self.at("if") and "if" not in stop:
            return self.parse_if(stop)
        if self.at("lambda") and "lambda" not in stop:
            return self.parse_lambda(stop)
        return self.parse_comp(stop)

    def parse_if(self, stop: set[str]) -> Term:
        self.expect("if")
        cond = self.parse_term(stop | {"then"})
        self.expect("then")
        then_branch = self.parse_term(stop | {"else"})
        self.expect("else")
        else_branch = self.parse_term(stop)
        return If(cond, then_branch, else_branch)

    def parse_lambda(self, stop: set[str]) -> Term:
        self.expect("lambda")
        param = self.expect_kind("ident").value
        self.expect(".")
        return Lam(param, self.parse_term(stop))

    def parse_comp(self, stop: set[str]) -> Term:
        left = self.parse_equal(stop | {"circ"})
        while self.at("circ") and "circ" not in stop:
            self.expect("circ")
            left = Comp(left, self.parse_equal(stop | {"circ"}))
        return left

    def parse_equal(self, stop: set[str]) -> Term:
        left = self.parse_app(stop | {"="})
        if self.at("=") and "=" not in stop:
            self.expect("=")
            return Equal(left, self.parse_app(stop))
        return left

    def parse_app(self, stop: set[str]) -> Term:
        left = self.parse_atom(stop)
        while self.starts_atom() and not self.stopped(stop):
            left = App(left, self.parse_atom(stop))
        return left

    def parse_atom(self, stop: set[str]) -> Term:
        token = self.current()
        if self.stopped(stop):
            raise ParseError(f"expected term at position {token.position}")
        if token.kind == "ident":
            self.index += 1
            return Var(token.value)
        if token.kind == "string":
            self.index += 1
            return NameConst(token.value)
        if self.at("id"):
            self.expect("id")
            return Id()
        if self.at("true"):
            self.expect("true")
            return BoolConst(True)
        if self.at("false"):
            self.expect("false")
            return BoolConst(False)
        if self.at("("):
            return self.parse_parenthesized(stop)
        raise ParseError(f"expected term at position {token.position}")

    def parse_parenthesized(self, stop: set[str]) -> Term:
        self.expect("(")
        inner = self.parse_term(stop | {"/", ")"})
        if self.at("/"):
            self.expect("/")
            name = self.expect_kind("ident").value
            self.expect(")")
            self.expect(".")
            return Ext(inner, name, self.parse_term(stop))
        self.expect(")")
        return inner

    def starts_atom(self) -> bool:
        token = self.current()
        return (
            token.kind in {"ident", "string"}
            or token.value in {"id", "true", "false", "("}
        )

    def stopped(self, stop: set[str]) -> bool:
        token = self.current()
        return token.kind in stop or token.value in stop

    def at(self, value: str) -> bool:
        return self.current().value == value

    def expect(self, value: str) -> Token:
        token = self.current()
        if token.value != value:
            raise ParseError(f"expected {value!r} at position {token.position}")
        self.index += 1
        return token

    def expect_kind(self, kind: str) -> Token:
        token = self.current()
        if token.kind != kind:
            raise ParseError(f"expected {kind} at position {token.position}")
        self.index += 1
        return token

    def current(self) -> Token:
        return self.tokens[self.index]
