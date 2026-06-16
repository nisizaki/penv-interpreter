from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Lam:
    param: str
    body: Term


@dataclass(frozen=True)
class App:
    fn: Term
    arg: Term


@dataclass(frozen=True)
class Id:
    pass


@dataclass(frozen=True)
class Ext:
    value_term: Term
    var: str
    env_term: Term


@dataclass(frozen=True)
class Comp:
    term: Term
    env_term: Term


@dataclass(frozen=True)
class NameConst:
    name: str


@dataclass(frozen=True)
class BoolConst:
    value: bool


@dataclass(frozen=True)
class If:
    cond: Term
    then_branch: Term
    else_branch: Term


@dataclass(frozen=True)
class Equal:
    left: Term
    right: Term


Term = Var | Lam | App | Id | Ext | Comp | NameConst | BoolConst | If | Equal
