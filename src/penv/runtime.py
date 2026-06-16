from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from penv.ast import Term


class PenvError(Exception):
    """Base exception for interpreter errors."""


class UnboundName(PenvError):
    """Raised when an environment has no binding for a name."""


class TypeMismatch(PenvError):
    """Raised when a value is used in an unsupported position."""


@dataclass(frozen=True)
class NameValue:
    name: str


@dataclass(frozen=True)
class BoolValue:
    value: bool


@dataclass(frozen=True)
class Closure:
    param: str
    body: Term
    env: Value


@dataclass(frozen=True)
class EnvValue:
    lookup_function: Callable[[str], Value]

    @classmethod
    def empty(cls) -> EnvValue:
        def lookup(name: str) -> Value:
            raise UnboundName(f"unbound name: {name}")

        return cls(lookup)

    def lookup(self, name: str) -> Value:
        return self.lookup_function(name)

    def extend(self, name: str, value: Value) -> EnvValue:
        parent = self

        def lookup(query: str) -> Value:
            if query == name:
                return value
            return parent.lookup(query)

        return EnvValue(lookup)


Value = NameValue | BoolValue | Closure | EnvValue
