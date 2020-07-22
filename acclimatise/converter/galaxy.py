import inspect
import tempfile
from io import IOBase, StringIO, TextIOBase
from os import PathLike
from pathlib import Path
from typing import Generator, List

from dataclasses import dataclass

from acclimatise import cli_types
from acclimatise.converter import NamedArgument, WrapperGenerator
from acclimatise.model import CliArgument, Command, Flag, Positional
from acclimatise.yaml import yaml

from galaxyxml.tool import Tool
from galaxyxml.tool.parameters import (
    BooleanParam,
    FloatParam,
    Inputs,
    IntegerParam,
    Outputs,
    Requirement,
    Requirements,
    Tests,
    TextParam
)


@dataclass
class GalaxyGenerator(WrapperGenerator):
    case = "snake"

    @classmethod
    def format(cls) -> str:
        return "galaxy"

    @property
    def suffix(self) -> str:
        return ".xml"

    def command_to_tool(self, cmd: Command) -> Tool:
        inputs: List[CliArgument] = [*cmd.named] + (
            [] if self.ignore_positionals else [*cmd.positional]
        )
        names = self.choose_variable_names(inputs)
        print(dir(cmd))
        print(cmd.command)
        tool = Tool(name = cmd.command[0], 
                    id = cmd.command[0],
                    version = "0.0.1",
                    description = "TODO", 
                    executable = None, 
                    version_command="%s %s" % (cmd.command[0], cmd.version_flag.full_name()))

        # TODO this could also be done via a macro, which would allow for
        # easier adaptions, e.g. adding other requirements without modifying
        # the autogenerated tool
        requirements = Requirements()
        requirements.append(Requirement('package', 'TODO_TOOLNAMEHERE',
                                             version='TODO_TOOLVERSION'))
        tool.requirements = requirements
        
        tool.command = ""  # TODO command line here

        tool.inputs = Inputs()
        tool.outputs = Outputs()

        for arg in names:
            assert arg.name != "", arg

            # TODO galaxy outputs don't have help
            # TODO galaxy outputs need different label
            args = dict(name=arg.name,
                        optional=False,
                        value="" if arg.arg.optional else "TODO_DEFAULT_VALUE",
                        label=arg.name,
                        help=arg.arg.description)

            if isinstance(arg.arg.get_type(), cli_types.CliFile):
                pass  # TODO 
            elif isinstance(arg.arg.get_type(), cli_types.CliDir):
                pass  # TODO
            elif isinstance(arg.arg.get_type(), cli_types.CliString):
                gxy_param_class = TextParam
            elif isinstance(arg.arg.get_type(), cli_types.CliFloat):
                args["min"] = None  # TODO
                args["max"] = None
                gxy_param_class = FloatParam
            elif isinstance(arg.arg.get_type(), cli_types.CliInteger):
                args["min"] = None
                args["max"] = None
                gxy_param_class = IntegerParam
            elif isinstance(arg.arg.get_type(), cli_types.CliBoolean):
                args["checked"]=False
                args["truevalue"]="TODO"
                args["falsevalue"]="TODO"
                gxy_param_class = BooleanParam
            elif isinstance(arg.arg.get_type(), cli_types.CliEnum):
                pass  # TODO
            elif isinstance(arg.arg.get_type(), cli_types.CliList):
                pass  # TODO
            elif isinstance(arg.arg.get_type(), cli_types.CliTuple):
                pass  # TODO
            else:
                raise Exception(f"Invalid type {typ}!")

            gxy_param = gxy_param_class(**args)

            if True:  # TODO we need to distinguish input / output files
                tool.inputs.append(gxy_param)
            else:
                tool.outputs.append(gxy_param)


        # TODO add tests
        tool.tests = Tests()

        tool.help = cmd.help_text

        return tool


    def save_to_string(self, cmd: Command) -> str:
        return self.command_to_tool(cmd).export().decode('utf-8')

    #def save_to_file(self, cmd: Command, path: Path) -> None:
    #    # Todo Can we remove this and simply rely on the implementation 
    #    # in the baseclass (WrapperGenerator)
    #    pass

    @classmethod
    def validate(cls, wrapper: str, cmd: Command = None, explore=True):
        # Todo add planemo lint call
        # probably calling the functions in this loop: https://github.com/galaxyproject/planemo/blob/2b659c9a7531f9a973e60d6319898e58ef3ea781/planemo/tool_lint.py#L28
        print("VALIDATE")
        pass
