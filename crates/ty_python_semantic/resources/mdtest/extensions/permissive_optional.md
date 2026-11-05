# Permissive optional values (prototype)

```toml
[environment]
python-version = "3.12"
```

## Portable Annotated metadata

The opt-in uses a standard annotation. Checkers that do not recognise this metadata still see the
underlying optional type.

```py
from typing import Annotated, TypeVar

T = TypeVar("T")
Maybe = Annotated[T | None, "anvil:permissive-optional"]
type NewMaybe[T] = Annotated[T | None, "anvil:permissive-optional"]
type StrictMaybe = str | None

def takes_str(value: str) -> None: ...
def direct(value: Annotated[str | None, "anvil:permissive-optional"]):
    reveal_type(value.upper())  # revealed: str
    takes_str(value)  # no diagnostic
    if value is None:
        reveal_type(value)  # revealed: None
        value.upper()  # error: [unresolved-attribute]
    else:
        reveal_type(value)  # revealed: str

def legacy_alias(value: Maybe[str]):
    reveal_type(value.upper())  # revealed: str

def new_alias(value: NewMaybe[str]):
    reveal_type(value.upper())  # revealed: str

def wrapped_alias(value: Annotated[StrictMaybe, "anvil:permissive-optional"]):
    reveal_type(value.upper())  # revealed: str

def unrelated(value: Annotated[str | None, "other metadata"]):
    value.upper()  # error: [unresolved-attribute]

def non_optional(value: Annotated[str, "anvil:permissive-optional"]):
    reveal_type(value)  # revealed: str

class Record:
    nickname: str | None

def nested_field(value: Annotated[Record | None, "anvil:permissive-optional"]):
    value.nickname.upper()  # error: [unresolved-attribute]

def container(values: Annotated[list[str | None], "anvil:permissive-optional"]):
    values[0].upper()  # error: [unresolved-attribute]
```

## Ordinary use and explicit None checks

A permissive optional retains the concrete result of an operation without requiring a guard. An
explicit None check still checks both branches.

```py
from typing import Annotated

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

def takes_str(value: str) -> None: ...
def example(value: Maybe[str]):
    reveal_type(value.upper())  # revealed: str
    takes_str(value)  # no diagnostic
    if value is None:
        reveal_type(value)  # revealed: None
        value.upper()  # error: [unresolved-attribute]
    else:
        reveal_type(value)  # revealed: str
```

## Proven None branches

Matching None proves that the value is absent, just as an identity check does.

```py
from typing import Annotated, Literal

def takes_str(value: str) -> None: ...
def example(value: Annotated[str | None, "anvil:permissive-optional"]):
    match value:
        case None as absent:
            reveal_type(value)  # revealed: None
            takes_str(value)  # error: [invalid-argument-type]
            value.upper()  # error: [unresolved-attribute]
            reveal_type(absent)  # revealed: None
            takes_str(absent)  # error: [invalid-argument-type]
        case _:
            reveal_type(value)  # revealed: str

def by_instance(value: Annotated[str | None, "anvil:permissive-optional"]):
    if isinstance(value, type(None)):
        reveal_type(value)  # revealed: None
        takes_str(value)  # error: [invalid-argument-type]

def by_exclusion(value: Annotated[str | None, "anvil:permissive-optional"]):
    if not isinstance(value, str):
        reveal_type(value)  # revealed: None
        takes_str(value)  # error: [invalid-argument-type]

def by_truthiness(value: Annotated[Literal["present"] | None, "anvil:permissive-optional"]):
    if not value:
        reveal_type(value)  # revealed: None
        takes_str(value)  # error: [invalid-argument-type]
```

## None proofs through generic bounds

A bound carries the policy through a type variable, including its None branches.

```py
from typing import Annotated

def takes_str(value: str) -> None: ...
def example[T: Annotated[str | None, "anvil:permissive-optional"]](value: T):
    if value is None:
        reveal_type(value)  # revealed: None
        takes_str(value)  # error: [invalid-argument-type]
        value.upper()  # error: [unresolved-attribute]
```

## Field types and propagation

The policy follows values through aliases, containers and generic functions. It does not make field
results dynamic or hide errors in their use.

```py
from typing import Annotated, Literal, TypeVar

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

class Record:
    def __getitem__(self, key: Literal["name"]) -> str:
        return "Alice"
    def __setitem__(self, key: Literal["name"], value: str | None) -> None: ...
    def update(self, *, name: str | None = None) -> None: ...

def read() -> Maybe[Record]: ...

T = TypeVar("T")

def identity(value: T) -> T:
    return value

def example():
    value = read()
    alias = value
    reveal_type(alias["name"])  # revealed: str
    reveal_type(identity(value)["name"])  # revealed: str
    reveal_type([value][0]["name"])  # revealed: str
    value["name"] = None  # no diagnostic
    value.update(name="Alice")  # no diagnostic
    value.update(name=42)  # error: [invalid-argument-type]
    value["name"] = 42  # error: [invalid-assignment]
    value["name"] + 42  # error: [unsupported-operator]
    value["name"].uppper()  # error: [unresolved-attribute]
    result = identity(value)
    if result is None:
        reveal_type(result)  # revealed: None
    else:
        reveal_type(result)  # revealed: Record
```

## Ordinary optional values remain strict

```py
from typing import Annotated

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

def example(value: str | None):
    value.upper()  # error: [unresolved-attribute]

def mixed(permissive: Maybe[str], strict: str | None, flag: bool):
    first = permissive if flag else strict
    second = strict if flag else permissive
    reveal_type(first)  # revealed: str | None
    first.upper()  # error: [unresolved-attribute]
    second.upper()  # error: [unresolved-attribute]

def mixed_containers(permissive: list[Maybe[str]], strict: list[str | None], flag: bool):
    first = permissive if flag else strict
    second = strict if flag else permissive
    first[0].upper()  # error: [unresolved-attribute]
    second[0].upper()  # error: [unresolved-attribute]
```

## Assigning and returning None

```py
from typing import Annotated

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

def absent() -> Maybe[str]:
    return None  # no diagnostic

def wrong() -> Maybe[str]:
    return 42  # error: [invalid-return-type]

def example(value: Maybe[str]):
    alias = value
    alias = None
    alias.upper()  # error: [unresolved-attribute]
```

## Gradual bounds

The uncertain None can be absent, but cannot represent an unrelated value.

```py
from typing import Annotated, Any
from ty_extensions import Bottom, Intersection, Not, Top

type Absent = Annotated[None, "anvil:permissive-optional"]

def bounds(top: Top[Absent], bottom: Bottom[Absent]):
    reveal_type(top)  # revealed: None
    reveal_type(bottom)  # revealed: Never

def existing_algebra(top: Top[Intersection[Any, None]], bottom: Bottom[Intersection[Any, None]]):
    reveal_type(top)  # revealed: None
    reveal_type(bottom)  # revealed: Never

def intersections(value: Bottom[Intersection[Absent, None]]):
    reveal_type(value)  # revealed: Never

def complement(top: Top[Not[Absent]], bottom: Bottom[Not[Absent]]):
    reveal_type(top)  # revealed: object
    reveal_type(bottom)  # revealed: ~None

def takes_absent(value: Absent) -> None: ...

absent: Absent = None  # no diagnostic
invalid: Absent = 42  # error: [invalid-assignment]
takes_absent(42)  # error: [invalid-argument-type]
```

## Calls and other ordinary operations

```py
from typing import Annotated
from collections.abc import Awaitable, Callable
from contextlib import AbstractContextManager

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

def example(
    callback: Maybe[Callable[[str], int]],
    number: Maybe[int],
    items: Maybe[list[str]],
):
    reveal_type(callback("Alice"))  # revealed: int
    callback(42)  # error: [invalid-argument-type]
    reveal_type(number + 1)  # revealed: int
    reveal_type(-number)  # revealed: int
    for item in items:
        reveal_type(item)  # revealed: str
    number > 0  # no diagnostic
    "Alice" in items  # no diagnostic

async def protocols(
    pending: Maybe[Awaitable[str]],
    manager: Maybe[AbstractContextManager[str]],
):
    reveal_type(await pending)  # revealed: str
    with manager as value:
        reveal_type(value)  # revealed: str
```

## Declared attributes

```py
from typing import Annotated

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

class Record:
    name: str

def write(value: Maybe[Record]):
    value.name = "Alice"  # no diagnostic
    value.name = 42  # error: [invalid-assignment]

def delete(value: Maybe[Record]):
    del value.name  # no diagnostic
```

## Subscript deletion

Deleting an item uses the same receiver policy as reading and writing items. Ordinary optional lists
and values proved to be None remain invalid receivers.

```py
from typing import Annotated

def delete(value: Annotated[list[str] | None, "anvil:permissive-optional"]):
    del value[0]  # no diagnostic
    if value is None:
        del value[0]  # error: [not-subscriptable]

def ordinary(value: list[str] | None):
    del value[0]  # error: [not-subscriptable]
```

## The policy does not track external state or relax other union members

```py
from typing import Annotated, Literal

type Maybe[T] = Annotated[T | None, "anvil:permissive-optional"]

class Record:
    nickname: str | None
    def __getitem__(self, key: Literal["name"]) -> str:
        return "Alice"

def read() -> Maybe[Record]: ...
def logout() -> None: ...
def mixed() -> Maybe[Record] | int: ...
def example():
    value = read()
    logout()
    value["name"]  # no diagnostic
    read()["name"]  # no diagnostic
    value.nickname.upper()  # error: [unresolved-attribute]
    if value is None:
        value["name"]  # error: [not-subscriptable]
        read()["name"]  # no diagnostic
    mixed()["name"]  # error: [not-subscriptable]
```
