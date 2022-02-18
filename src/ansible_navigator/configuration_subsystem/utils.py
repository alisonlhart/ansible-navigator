"""Utilities related to the configuration subsystem."""

import sys

from types import SimpleNamespace
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union

from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Constants as C
from .definitions import SettingsEntry


class HumanReadableEntry(NamedTuple):
    """Data structure for a setting entry."""

    #: The possible values
    choices: List
    #: The CLI parameters, short and long
    cli_parameters: Dict[str, str]
    #: The path to the current settings file
    current_settings_file: str
    #: The current, effective value
    current_value: Union[bool, Dict, str, List]
    #: The default value
    default: Union[bool, str]
    #: A short description
    description: str
    #: The environment variable
    env_var: str
    #: Indicate if the current == the default
    is_default: bool
    #: The name
    name: str
    #: A sample settings file snippet
    settings_file_sample: Union[str, Dict]
    #: The source of the current value
    source: str


def transform_settings(
    settings: ApplicationConfiguration,
) -> List[Dict[str, Union[bool, Dict, str, List]]]:
    """Transform the current settings into a list of dictionaries.

    :param settings: The current settings
    :returns: The settings represented as a list of dictionaries
    """
    settings_list = []

    entry = _settings_file_entry(settings.internals)
    settings_list.append(entry._asdict())

    for current in settings.entries:
        application_name = settings.application_name
        settings_file_path = settings.internals.settings_file_path
        entry = _standard_entry(
            current=current,
            application_name=application_name,
            settings_file_path=settings_file_path,
        )
        # py36, py37 dataclass._asdict returns OrderedDict
        if sys.version_info >= (3, 8):
            entry_as_dict = entry._asdict()
        else:
            entry_as_dict = dict(entry._asdict())
        settings_list.append(entry_as_dict)

    sorted_settings = sorted(settings_list, key=lambda d: d["name"])
    return sorted_settings


def _sample_generator(settings_path: str) -> Dict[str, Union[Dict, str]]:
    """Generate a settings file sample.

    :param settings_path: The dot delimited settings file path for a settings entry
    :returns: A sample of the settings file
    """
    if "." not in settings_path:
        return {settings_path: "<------"}
    key, remainder = settings_path.split(".", 1)
    return {key: _sample_generator(remainder)}


def _settings_file_entry(internals: SimpleNamespace) -> HumanReadableEntry:
    """Generate a dictionary containing the details for the settings file.

    :param internals: The internal storage for settings information
    :returns: The settings file entry
    """
    source = internals.settings_source
    if source is C.SEARCH_PATH:
        is_default = True
    elif source is C.NONE or source is C.ENVIRONMENT_VARIABLE:
        is_default = False

    default = (
        "{CWD}/ansible-navigator.{ext} or {HOME}/.ansible-navigator.{ext}"
        " where ext is yml, yaml or json"
    )

    return HumanReadableEntry(
        choices=[],
        cli_parameters={"short": "None", "long": "None"},
        current_settings_file=internals.settings_file_path or "None",
        current_value=internals.settings_file_path or "None",
        default=default,
        is_default=is_default,
        description="The path to the current settings file",
        name="current_settings_file",
        env_var="ANSIBLE_NAVIGATOR_CONFIG",
        settings_file_sample="Not applicable",
        source=internals.settings_source.value,
    )


def _standard_entry(
    current: SettingsEntry,
    application_name: str,
    settings_file_path: str,
) -> HumanReadableEntry:
    """Generate a dictionary containing the details for one settings entry.

    :param current: A settings entry
    :param application_name: The applications name
    :param settings_file_path: The current settings file path
    :return: The settings file entry
    """
    if isinstance(current.cli_parameters, CliParameters):
        cli_long = current.cli_parameters.long_override or f"--{current.name_dashed}"

        if current.cli_parameters.short:
            cli_short = current.cli_parameters.short
        else:
            cli_short = "No short CLI parameter"

    else:
        cli_long = "No long CLI parameter"
        cli_short = "No short CLI parameter"

    if isinstance(current.value.current, C):
        current_value = current.value.current.value
    else:
        current_value = current.value.current

    if isinstance(current.value.default, C):
        default = current.value.default.value
    else:
        default = current.value.default

    env_var = current.environment_variable(application_name.upper())

    is_default = current.value.source in (C.NOT_SET, C.DEFAULT_CFG)

    settings_file_sample = _sample_generator(
        current.settings_file_path(prefix=application_name.replace("-", "_")),
    )

    return HumanReadableEntry(
        choices=list(current.choices),  # May be a tuple e.g. PLUGIN_TYPES
        cli_parameters={"short": cli_short, "long": cli_long},
        current_settings_file=settings_file_path or "None",
        current_value=current_value,
        default=default,
        description=current.short_description,
        env_var=env_var,
        is_default=is_default,
        name=current.name,
        settings_file_sample=settings_file_sample,
        source=current.value.source.value,
    )