from __future__ import annotations

import contextlib
import importlib
import inspect
import random
import typing
from types import ModuleType
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import typing_extensions
from typing_extensions import NotRequired, TypedDict

T = TypeVar("T")
TD = TypeVar("TD", bound=TypedDict)


class _Missing:
    ...


MISSING = _Missing()


def _resolve_bases(cls: type) -> List[type]:
    _get_globals(inspect.getmodule(cls))
    return cls.__orig_bases__  # type: ignore


def _get_type_hints(type_: Type[Any]) -> Dict[str, Any]:
    # I'm not really sure as to if there is a better way to do this

    origin: Optional[type] = typing.get_origin(type_)

    if origin is None:
        origin = type_

    module = inspect.getmodule(origin)
    if Generic not in origin.__bases__:
        globals_ = _get_globals(module)
    else:
        globals_ = _get_generic_globals(type_, origin, module)

    return typing.get_type_hints(origin, globals_)


def _get_generic_globals(type_: type, origin: type, module: Optional[ModuleType]):
    bases = _resolve_bases(origin)  # Find the bases of the class
    generic = next(base for base in bases if typing.get_origin(base) is Generic)
    # Get the Generic[...] base
    args: Tuple[TypeVar, ...] = typing.get_args(
        generic
    )  # Find the TypeVars in the Generic
    mapping = dict(zip(args, typing.get_args(type_)))
    names: Dict[str, TypeVar] = {arg.__name__: mapping[arg] for arg in args}
    globals_ = _get_globals(module)

    for key, value in globals_.items():
        with contextlib.suppress(TypeError):
            if isinstance(value, TypeVar):
                globals_[key] = names[value.__name__]
    return globals_


cache: Dict[ModuleType, Dict[str, Any]] = {}


def _get_globals(module: Optional[ModuleType]):
    if module:

        if module in cache:
            return cache[module]

        # Because it is already initialized we can now set typing.TYPE_CHECKING to True
        typing.TYPE_CHECKING = True

        try:
            importlib.reload(module)
            # Reload it, which allows all the imports to be reevaluated
        finally:
            typing.TYPE_CHECKING = False

        cache[module] = module.__dict__
    # If we would not do this there would be missing globals that are needed to evaluate the type hints
    # This is only needed because of potential `from __future__ import annotations` imports
    return module.__dict__


def not_required(type_: Type[Any]) -> bool:
    # Check if type is NotRequired
    return typing_extensions.get_origin(type_) is NotRequired


def optional(type_: Type[Any]) -> bool:
    # Check if type is Optional
    return type(None) in typing_extensions.get_args(type_)


def _generate_primitive(type_: Type[T]) -> T:
    return type_()


def _generate_list(key: str, type_: Type[T]) -> List[T]:

    return []


def _generate_field(key: str, value: Any) -> Any:
    origin = typing_extensions.get_origin(value)
    args = typing_extensions.get_args(value)

    if origin is None:
        # Generics don't have an origin, this includes TypedDict and "primitives"
        if typing_extensions.is_typeddict(value):
            return generate(value)
        return _generate_primitive(value)

    elif origin is Literal:
        # Pick a random arg of the Literal
        return random.choice(args)

    elif origin is Union:
        return None

    elif not_required(value):
        return MISSING

    elif issubclass(origin, Sequence):
        # If the origin is a Sequence, generate a list
        # This is type agnostic, which is technically wrong because it causes all
        # Sequences to be treated as Lists
        return _generate_list(key, args[0])

    elif origin is dict:
        # A type hint for a dict is pretty useless because no information about it can be inferred
        # We return an empty dict and hope for the best
        return {}

    return MISSING


def generate_union(type_: Any) -> Any:
    # This works as an entry point generator for unions
    if len(typing.get_args(type_)) > 1:
        return [generate(arg) for arg in typing.get_args(type_)]


def generate(type_: Type[TD]) -> TD:
    """Generate a random object of the given typed dict

    Parameters
    ----------
    type_ : Type[TD]
        The type of the object to generate
    constraints : Optional[Constraints]
        What constraints to apply to the generated object

    Returns
    -------
    TD
        The generated object
    """

    typehints = _get_type_hints(type_)

    data = {}
    for key, value in typehints.items():
        val = _generate_field(key, value)
        if val is not MISSING:
            data[key] = val

    _check_obj(typehints, data)

    return cast(TD, data)


def _check_obj(typehints: Dict[str, Any], data: Dict[str, Any]) -> None:
    """Check that all required fields are present

    Parameters
    ----------
    typehints : dict
        The type hints for the class
    data : dict
        The generated data

    Raises
    ------
    RuntimeError
        If a required field is missing
    """
    required_keys = {
        key
        for key, value in typehints.items()
        if typing.get_origin(value) is not NotRequired
    }
    if not required_keys.issubset(data.keys()):
        raise RuntimeError(
            (
                f"Missing required keys: {required_keys - data.keys()}. This is a bug, please report it."
            )
        )
