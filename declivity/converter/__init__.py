from abc import abstractmethod
from declivity.model import Command, CliArgument
from dataclasses import dataclass


@dataclass
class WrapperGenerator:
    """
    Abstract base class for a class that converts a Command object into a string that defines a tool
    wrapper in a certain workflow language
    """

    @abstractmethod
    def generate_wrapper(self, cmd: Command) -> str:
        """
        Abstract method that defines the interface for converting a Command into a wrapper string
        """
        pass

    def choose_variable_name(self, flag: CliArgument, format='snake') -> str:
        """
        Choose a name for this flag (e.g. the variable name when this is used to generate code), based on whether
        the user wants an auto generated one or not
        """
        if self.generate_names:
            return flag.generate_name()
        elif format == 'snake':
            return flag.name_to_snake()
        elif format == 'camel':
            return flag.name_to_camel()

    generate_names: bool = False
    """
    Rather than using the long flag to generate the argument name, generate them automatically using the
    flag description. Generally helpful if there are no long flags, only short flags.
    """

    ignore_positionals: bool = False
    """
    Don't include positional arguments, for example because the help formatting has some
    misleading sections that look like positional arguments
    """
