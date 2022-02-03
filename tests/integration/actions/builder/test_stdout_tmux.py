"""Tests for ``config`` from CLI, stdout."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._interactions import add_indicies
from .base import BUIDLER_FIXTURE
from .base import BaseClass


class StdoutCommand(Command):
    """stdout command"""

    subcommand = "builder"
    preclear = True


class ShellCommand(Step):
    """a shell command"""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="builder help-builder with ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["usage: ansible-builder [-h]"],
    ),
    ShellCommand(
        comment="builder help-builder without ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["usage: ansible-builder [-h]"],
    ),
    ShellCommand(
        comment="builder help-builder fail with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="interactive",
            execution_environment=True,
        ).join(),
        look_fors=["--hb or --help-builder is valid only when 'mode' argument is set to 'stdout'"],
    ),
    ShellCommand(
        comment="builder help-builder fail with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="interactive",
            execution_environment=False,
        ).join(),
        look_fors=["--hb or --help-builder is valid only when 'mode' argument is set to 'stdout'"],
    ),
    ShellCommand(
        comment="build execution-environment without ee",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime \
                     docker -v 3  --workdir {BUIDLER_FIXTURE}",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["Hello from EE", "The build context can be found at"],
    ),
    ShellCommand(
        comment="build execution-environment with ee",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime docker -v 3 \
                     --workdir {BUIDLER_FIXTURE}",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["Hello from EE", "The build context can be found at"],
    ),
    ShellCommand(
        comment="build execution-environment without ee in interactive mode",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime docker -v 3 \
                      --workdir {BUIDLER_FIXTURE}",
            mode="interactive",
            execution_environment=False,
        ).join(),
        look_fors=[
            "Subcommand 'builder' does not support mode 'interactive'. \
                   Supported modes: 'stdout'.",
        ],
    ),
    ShellCommand(
        comment="build execution-environment with ee in interactive mode",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime docker -v 3 \
                      --workdir {BUIDLER_FIXTURE}",
            mode="interactive",
            execution_environment=True,
        ).join(),
        look_fors=[
            "Subcommand 'builder' does not support mode 'interactive'. \
                Supported modes: 'stdout'.",
        ],
    ),
)

steps = add_indicies(stdout_tests)


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``builder`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
