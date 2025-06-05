import pytest
from pytest import MonkeyPatch

from src.utils import get_nonempty_string_input, get_valid_int_input, get_valid_user_input

def test_get_valid_user_input(monkeypatch: MonkeyPatch, capsys):

    valid_answers = ("One", "Two")
    input_values = ("", "Three", "Two")

    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))

    result = get_valid_user_input("Enter a str: ", valid_answers, "This is invalid.")
    captures = capsys.readouterr()

    assert result in valid_answers
    assert captures.out == "This is invalid.\nThis is invalid.\n"


def test_get_nonempty_string_input(monkeypatch: MonkeyPatch, capsys):
    input_values = ("", "", "Ok")

    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    result = get_nonempty_string_input("Enter a str: ", "This is invalid.")
    captures = capsys.readouterr()

    assert result != ""
    assert captures.out == "This is invalid.\nThis is invalid.\n"


def test_get_valid_int_input_validentry(monkeypatch: MonkeyPatch, capsys):
    input_values = ("1", "not needed")

    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    result = get_valid_int_input("Enter a int: ", 1, True, True)
    captures = capsys.readouterr()

    assert result == [1]
    assert captures.out == ""


def test_get_valid_int_input_validentry_as_third_try_True_False(monkeypatch: MonkeyPatch, capsys):
    #We expected 3 int separated by space, >0, in any order
    input_values = ("-2 2 4", "2 1 0", "1 3 2")
 
    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    result = get_valid_int_input("Enter 3 int: ", 3, True, False)
    captures = capsys.readouterr()

    assert result == [1, 3, 2]
    assert len(captures.out.split('\n')) == 3


def test_get_valid_int_input_validentry_as_third_try_False_True(monkeypatch: MonkeyPatch, capsys):
    #We expected any 3 int separated by space, in ascending order
    input_values = ("not valid", "2 1 6", "-4 -2 0")
 
    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    result = get_valid_int_input("Enter 3 int: ", 3, False, True)
    captures = capsys.readouterr()

    assert result == [-4, -2, 0]
    assert len(captures.out.split('\n')) == 3


def test_get_valid_int_input_validentry_as_third_try_False_False(monkeypatch: MonkeyPatch, capsys):
    #We expected any 3 int separated by space, in any order
    input_values = ("not valid", "2 3.2 0", "-5 12 3")
 
    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    result = get_valid_int_input("Enter 3 int: ", 3, False, False)
    captures = capsys.readouterr()

    assert result == [-5, 12, 3]
    assert len(captures.out.split('\n')) == 3


def test_get_valid_int_input_validentry_as_third_try_True_True(monkeypatch: MonkeyPatch, capsys):
    #We expected any 3 int separated by space, in any order
    input_values = ("not valid", "2 3.2 0", "3 12 26")
 
    input_generator = iter(input_values)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    result = get_valid_int_input("Enter 3 int: ", 3, True, True)
    captures = capsys.readouterr()

    assert result == [3, 12, 26]
    assert len(captures.out.split('\n')) == 3