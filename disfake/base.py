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
        return typing_extensions.get_origin(type_) is NotRequired

    def _optional(self, type_) -> bool:
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
            if typing_extensions.is_typeddict(value):
                return self._generate(value)
            return self._generate_primitive(value)

        elif origin is Literal:
            return random.choice(args)

        elif origin is Union:
            if self._optional(value):
                return None
            return (
                None if None in args else self._generate_field(key, random.choice(args))
            )
        elif origin is NotRequired:
            if self.sparse:
                return MISSING
            return random.choice([MISSING, self._generate_field(key, args[0])])

        elif issubclass(origin, Sequence):
            return self._generate_list(key, args[0])

        elif origin is dict:
            return {}

        return MISSING

    def generate_union(self, type_: Any) -> Any:
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

        typehints = self._get_type_hints(type_)

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

    def _get_type_hints(self, type_: Type) -> Dict[str, Any]:
        module = inspect.getmodule(type_)
        if module:
            typing.TYPE_CHECKING = True

            try:
                importlib.reload(module)
            finally:
                typing.TYPE_CHECKING = False
        globals_ = module.__dict__
        return typing.get_type_hints(type_, globals_)
