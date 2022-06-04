#!/usr/bin/env python3
"""This module provides the zk CLI"""
# zk/cli.py
__author__ = "Bert Hu"
__copyright__ = "Copyright 2022"
__credits__ = ["Bert Hu"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Bert Hu"
__email__ = ""
__status__ = "Production"


from typing import Optional
from pathlib import Path

import typer
from zk import __app_name__, __version__, DEFAULT_EDITOR
from zk import SUCCESS, WRITE_ERROR, CONFIG_ERROR
from zk import CONFIG_FILE_NAME
from zk import (
    FLEETING, DAILY, MEETING, LITERATURE, PERMANENT
)
from zk.config import ZettelConfig
from zk.config import write_new_config
from zk.config import ErrorResponse
from zk import zk

import subprocess

app = typer.Typer()
CONFIG_FILE_PATH = Path.home().joinpath(CONFIG_FILE_NAME)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


version_option = typer.Option(
    None,
    "--version", "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
)


@app.callback()
def main(
    version: Optional[bool] = version_option
) -> None:
    return


topic_option = typer.Option(
    '',
    '--topic', '-t',
    help="Add a topic string to end of new ZK file.",
)


@app.command()
def init() -> None:
    """Initialize the config file in home directory.

    Args:

    Returns:
        None:
    """
    err = write_new_config(CONFIG_FILE_PATH)
    if err.error == SUCCESS:
        typer.secho(
            f'Config file written to {CONFIG_FILE_PATH}',
            fg=typer.colors.GREEN,
        )

    return


def edit_callback(editor: bool):
    if editor:
        return DEFAULT_EDITOR
    return editor


edit_option = typer.Option(
    False,
    "--edit", "-e",
    help='Edit with specified editor',
    callback=edit_callback
)


def edit_prompt(edit: bool, file_path: Path) -> None:
    if edit and file_path != Path():
        editor = input(f'Edit file? [default: {DEFAULT_EDITOR}] ')
        editor = DEFAULT_EDITOR if editor == '' else editor
        try:
            subprocess.call([editor, file_path])
        except OSError:
            typer.secho(f'Editor  {editor}   not found.', fg=typer.colors.RED)


@app.command()
def daily(
    edit: Optional[bool] = edit_option,
) -> None:
    """Create a daily note.

    Args:
        edit (Optional[bool]): edit

    Returns:
        None:
    """
    error_resp = _write_note(DAILY)
    if error_resp.error == SUCCESS:
        typer.secho(error_resp.msg, fg=typer.colors.GREEN)
    else:
        typer.secho(error_resp.msg, fg=typer.colors.BRIGHT_RED)

    edit_prompt(edit, error_resp.doc)
    return


@app.command()
def fleet(
    topic: str = typer.Argument(''),
    edit: Optional[bool] = edit_option,
) -> None:
    """Create a fleeting note with optional[TOPIC].

    Args:
        topic (str): topic
        edit (Optional[bool]): edit

    Returns:
        None:
    """
    error_resp = _write_note(FLEETING, topic)
    if error_resp.error == SUCCESS:
        typer.secho(error_resp.msg, fg=typer.colors.GREEN)
    else:
        typer.secho(error_resp.msg, fg=typer.colors.BRIGHT_RED)

    edit_prompt(edit, error_resp.doc)
    return


@app.command()
def perm(
    topic: str = typer.Argument(...),
    edit: Optional[bool] = edit_option,
) -> None:
    """Create a permanent note with required[TOPIC].

    Args:
        topic (str): topic
        edit (Optional[bool]): edit

    Returns:
        None:
    """
    error_resp = _write_note(PERMANENT, topic)
    if error_resp.error == SUCCESS:
        typer.secho(error_resp.msg, fg=typer.colors.GREEN)
    else:
        typer.secho(error_resp.msg, fg=typer.colors.BRIGHT_RED)

    edit_prompt(edit, error_resp.doc)
    return


@app.command()
def lit(
    topic: str = typer.Argument(...),
    edit: Optional[bool] = edit_option,
) -> None:
    """Create a literature note with required[TOPIC].

    Args:
        topic (str): topic
        edit (Optional[bool]): edit

    Returns:
        None:
    """
    error_resp = _write_note(LITERATURE, topic)
    if error_resp.error == SUCCESS:
        typer.secho(error_resp.msg, fg=typer.colors.GREEN)
    else:
        typer.secho(error_resp.msg, fg=typer.colors.BRIGHT_RED)

    edit_prompt(edit, error_resp.doc)
    return


@app.command()
def meet(
    topic: str = typer.Argument(...),
    edit: Optional[bool] = edit_option,
) -> None:
    """Create a meeting note with required[TOPIC].

    Args:
        topic (str): topic
        edit (Optional[bool]): edit

    Returns:
        None:
    """
    error_resp = _write_note(MEETING, topic)
    if error_resp.error == SUCCESS:
        typer.secho(error_resp.msg, fg=typer.colors.GREEN)
    else:
        typer.secho(error_resp.msg, fg=typer.colors.BRIGHT_RED)

    edit_prompt(edit, error_resp.doc)
    return


def _write_note(note_type: int, topic: str = '') -> ErrorResponse:
    if CONFIG_FILE_PATH.is_file():
        zk_config = ZettelConfig(CONFIG_FILE_PATH)
        if zk_config.config_err_resp.error != SUCCESS:
            return zk_config.config_err_resp
    else:  # config file does not exist
        return ErrorResponse(CONFIG_ERROR,
                             'Config File not found. Please run zk init')
    librarian = _get_librarian(zk_config)
    write_path = librarian.get_write_path(note_type, topic)
    # if exists, return
    if write_path.exists():
        return ErrorResponse(WRITE_ERROR, f'Daily note {write_path} exists.',
                             write_path)
    else:
        note_path = librarian.write_note(note_type, topic)
        return ErrorResponse(SUCCESS, f'Note written to {note_path}.',
                             note_path)


def _get_librarian(zk_config: ZettelConfig) -> zk.Librarian:
    return zk.Librarian(zk_config)
