from __future__ import annotations

import importlib
import inspect
import random
import typing
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Sequence,
    Type,
    TypeVar,
    Union,
)

import typing_extensions
from typing_extensions import NotRequired, TypedDict

if TYPE_CHECKING:
    from .state import State

T = TypeVar("T")
TD = TypeVar("TD", bound=TypedDict)


class _Missing:
    ...


MISSING = _Missing()


def _get_type_hints(type_: Type) -> Dict[str, Any]:
    # I'm not really sure as to if there is a better way to do this

    # Get the module
    module = inspect.getmodule(type_)
    globals_ = _get_globals(module)
    return typing.get_type_hints(type_, globals_)


def _get_globals(module):
    if module:
        # Because it is already initialized we can now set typing.TYPE_CHECKING to True
        typing.TYPE_CHECKING = True

        try:
            importlib.reload(module)
            # Reload it, which allows all the imports to be reevaluated
        finally:
            typing.TYPE_CHECKING = False

    # If we would not do this there would be missing globals that are needed to evaluate the type hints
    # This is only needed because of potential `from __future__ import annotations` imports
    return module.__dict__
    # TODO: Check if using typing_extensions.get_type_hints works better with special types


class Base:
    def __init__(self, state: State, sparse: bool = True) -> None:
        """Generate a random object of the given type

        Parameters
        ----------
        state: State
            The state to use, only needed for subclasses
        sparse : bool, optional
            Whether the generated object should be sparse, by default True

            Setting this to `True` will skip non required fields, optional fields will be set to None and lists will be empty
            Setting this to `False` may cause in unexpected results or errors
        """
        self.state = state
        self.sparse = sparse

    def _not_required(self, type_) -> bool:
        # Check if type is NotRequired
        return typing_extensions.get_origin(type_) is NotRequired

    def _optional(self, type_) -> bool:
        # Check if type is Optional
        return type(None) in typing_extensions.get_args(type_)

    def _generate_primitive(self, type_: Type[T]) -> T:
        return type_()

    def _generate_list(self, key: str, type_: Type[T]) -> List[T]:
        if self.sparse:
            return []
        return [self._generate_field(key, type_) for _ in range(random.randint(1, 5))]  # type: ignore

    def _generate_field(self, key: str, value: Any):
        origin = typing_extensions.get_origin(value)
        args = typing_extensions.get_args(value)

        if origin is None:
            # Generics don't have an origin, this includes TypedDict and "primitives"
            if typing_extensions.is_typeddict(value):
                return self._generate(value)
            return self._generate_primitive(value)

        elif origin is Literal:
            # Pick a random arg of the Literal
            return random.choice(args)

        elif origin is Union:
            if self._optional(value) and self.sparse:
                return None

            return self._generate_field(key, random.choice(args))

        elif self._not_required(value):
            if self.sparse:
                # MISSING will cause the field to be skipped
                return MISSING
            # Else cause an empty field or generate the arg
            return random.choice([MISSING, self._generate_field(key, args[0])])

        elif issubclass(origin, Sequence):
            # If the origin is a Sequence, generate a list
            # This is type agnostic, which is technically wrong because it causes
            # Sequences to be treated as Lists
            return self._generate_list(key, args[0])

        elif origin is dict:
            # A type hint for a dict is pretty useless because no information about it can be inferred
            # We return an empty dict and hope for the best
            return {}

        return MISSING

    def generate_union(self, type_: Any) -> Any:
        # This works as an entry point generator for unions
        if len(typing.get_args(type_)) > 1:
            return [self._generate(arg) for arg in typing.get_args(type_)]

    def _generate(self, type_: Type[TD]) -> TD:
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
            val = self._generate_field(key, value)
            if val is not MISSING:
                data[key] = val

        self._check_obj(typehints, data)

        return data  # type: ignore

    def _check_obj(self, typehints: dict, data: dict) -> None:
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
            raise RuntimeError((f"Missing required keys: {required_keys - data.keys()}. This is a bug, please report it."))  # type: ignore
