"""Unit tests for the ``settings`` action."""

import curses

from ansible_navigator.actions.settings import color_menu
from ansible_navigator.actions.settings import content_heading
from ansible_navigator.actions.settings import filter_content_keys
from ansible_navigator.ui_framework.curses_defs import CursesLinePart


def test_color_menu_true():
    """Test color menu for a val set to the default."""
    entry = {"is_default": True}
    assert color_menu(0, "", entry) == (2, 0)


def test_color_menu_false():
    """Test color menu for a val not set to default."""
    entry = {"is_default": False}
    assert color_menu(0, "", entry) == (3, 0)


def test_content_heading_true():
    """Test menu generation for a defaulted value."""
    line_length = 100
    default_value = "default_value"
    current_value = default_value
    obj = {
        "name": "test settings entry",
        "current_value": current_value,
        "default": default_value,
        "is_default": current_value == default_value,
        "option": "test_option",
    }
    heading = content_heading(obj, line_length)
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"test settings entry (current/default: {default_value})" in heading[0][0].string
    assert heading[0][0].color == curses.COLOR_GREEN
    assert heading[0][0].column == 0


def test_content_heading_false() -> None:
    """Test menu generation for a value not default."""
    line_length = 100
    current_value = "current_value"
    default_value = "default_value"
    obj = {
        "name": "test settings entry",
        "current_value": current_value,
        "default": default_value,
        "is_default": current_value == default_value,
        "option": "test_option",
    }
    heading = content_heading(obj, line_length)
    assert heading
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert (
        f"test settings entry (current: {current_value})  (default: {default_value})"
        in heading[0][0].string
    )
    assert heading[0][0].color == curses.COLOR_YELLOW
    assert heading[0][0].column == 0


def test_filter_content_keys() -> None:
    """Test filtering keys."""
    obj = {"__key": "value", "key": "value"}
    ret = {"key": "value"}
    assert filter_content_keys(obj) == ret
