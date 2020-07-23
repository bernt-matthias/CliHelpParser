"""
Contains the objects that represent a "type" of data a flag argument might store
"""
import typing
from enum import Enum

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class CliType:
    """
    A data type used in the command-line
    """

    default: Optional[typing.Any] = None
    """
    A default value, None if unknown
    """

    @property
    def representable(self) -> set:
        """
        Returns a set of types that this type could alternatively be represented as.
        Adds the class's own type to the _representable set
        """
        return self._representable.union({type(self)})

    # The list of types that this specific type could be representable as
    _representable = set()


@dataclass(unsafe_hash=True)
class CliEnum(CliType):
    """
    One of a list of possible options
    """

    default: Optional[Enum] = None
    """
    A default value, None if unknown
    """

    enum: Enum
    """
    The possible options as a Python Enum
    """


@dataclass(unsafe_hash=True)
class CliFloat(CliType):
    """
    Takes a floating-point value
    """

    default: Optional[float] = None
    """
    A default value, None if unknown
    """


@dataclass(unsafe_hash=True)
class CliInteger(CliType):
    """
    Takes an integer value
    """

    default: Optional[int] = None
    """
    A default value, None if unknown
    """

    _representable = {CliFloat}


@dataclass(unsafe_hash=True)
class CliString(CliType):
    """
    Takes a string value
    """

    default: Optional[str] = None
    """
    A default value, None if unknown
    """


@dataclass(unsafe_hash=True)
class CliBoolean(CliType):
    """
    Takes a boolean value
    """

    default: Optional[bool] = None
    """
    A default value, None if unknown
    """


@dataclass(unsafe_hash=True)
class CliDir(CliType):
    """
    Takes a directory path
    """

    default: Optional[str] = None
    """
    A default value, None if unknown
    """


@dataclass(unsafe_hash=True)
class CliFile(CliType):
    """
    Takes a file path
    """

    default: Optional[str] = None
    """
    A default value, None if unknown
    """


@dataclass(unsafe_hash=True)
class CliDict(CliType):
    """
    Takes a dictionary value
    """

    default: Optional[str] = None
    """
    A default value, None if unknown
    """

    key: CliType
    """
    Data type of the keys to this dictionary
    """

    value: CliType
    """
    Data type of the values to this dictionary
    """


@dataclass(unsafe_hash=True)
class CliList(CliType):
    """
    Takes a list value
    """

    default: Optional[typing.List[CliType]] = None
    """
    A default value, None if unknown
    """

    value: CliType
    """
    Data type of the values in this list
    """


@dataclass(unsafe_hash=True)
class CliTuple(CliType):
    """
    Takes a list of values with a fixed length, possibly each with different types
    """

    default: Optional[typing.Tuple[CliType]] = None

    """
    A default value, None if unknown
    """

    values: typing.List[CliType]
    """
    List of types, in order, held within the tuple
    """

    @property
    def homogenous(self):
        """
        A tuple is homogenous if all types in the tuple are the same, aka the set of all types has length 1
        """
        return len(set([type(x) for x in self.values])) == 1
