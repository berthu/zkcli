#!/usr/bin/env python3
"""This module provideAs the config manager for zk controller."""
# zk/config.py
__author__ = "Bert Hu"
__copyright__ = "Copyright 2022"
__credits__ = ["Bert Hu"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Bert Hu"
__email__ = ""
__status__ = "Production"

from typing import NamedTuple
from configparser import ConfigParser
from pathlib import Path
from zk import (
    SUCCESS,
    WRITE_ERROR,
    CONFIG_ERROR,
    PATH_ERROR,
)  # status: ints
from zk import (
    TEMPLATES,
)  # note_type: ints
from zk import (
    NOTE_TYPES, DEFAULT_FOLDERS, DEFAULT_TEMPLATE_NAMES,
)  # dicts
from zk import (
    CONF_SEC_GENERAL,
    CONF_FIELD_ZETTEL_PATH,
    CONF_FIELD_TEMPLATE_REL_DIR,
    CONF_SEC_TEMPLATE_NAMES,
    CONF_SEC_NOTE_DIR_NAMES,
)  # str


class DocumentPath(NamedTuple):
    note_type: int
    path: Path


class ErrorResponse(NamedTuple):
    error: int
    msg: str
    doc: Path = Path()


def generate_default_config_parser() -> ConfigParser:
    default_parser = ConfigParser(delimiters=(':'))
    default_parser.optionxform = str
    default_parser[CONF_SEC_GENERAL] = {
        CONF_FIELD_ZETTEL_PATH: '~/Zettel',
        CONF_FIELD_TEMPLATE_REL_DIR: DEFAULT_FOLDERS[TEMPLATES],
    }
    default_parser[CONF_SEC_TEMPLATE_NAMES] = \
        dict(
            [
                (NOTE_TYPES[note_type], DEFAULT_TEMPLATE_NAMES[note_type])
                for note_type in NOTE_TYPES
            ]
        )
    default_parser[CONF_SEC_NOTE_DIR_NAMES] = \
        dict(
            [
                (NOTE_TYPES[note_type], DEFAULT_FOLDERS[note_type])
                for note_type in NOTE_TYPES
            ]
        )
    return default_parser


def write_new_config(config_file_path: Path) -> ErrorResponse:
    if config_file_path.is_file():
        return ErrorResponse(WRITE_ERROR, f'{config_file_path} exists.')
    else:
        default_config_parser = generate_default_config_parser()
        try:
            with config_file_path.open('w') as file:
                default_config_parser.write(file)
        except OSError:
            return ErrorResponse(WRITE_ERROR,
                                 'Error writing to {config_file_path}')
        return ErrorResponse(SUCCESS, '')


class ZettelConfig:
    """responsible for creating, reading, and checking config file contents.
    """

    def __init__(self, config_path: Path) -> None:
        config_parser = self._read_config(config_path)
        default_parser = generate_default_config_parser()
        self.config_err_resp = self.check_config_parser(config_parser,
                                                        default_parser)
        self.zettel_path = Path()
        self.template_paths, self.write_dir_paths = {}, {}
        if self.config_err_resp.error == SUCCESS:
            self.zettel_path = self._get_zettel_path(config_parser)
            self.template_paths = dict(
                [DocumentPath(
                    note_type,
                    self._get_template_path(config_parser, note_type)
                ) for note_type in NOTE_TYPES]
            )
            self.write_dir_paths = dict(
                [DocumentPath(
                    note_type,
                    self._get_write_dir_path(config_parser, note_type)
                ) for note_type in NOTE_TYPES]
            )

    def _get_zettel_path(self, config_parser: ConfigParser) -> Path:
        return Path(config_parser[CONF_SEC_GENERAL][CONF_FIELD_ZETTEL_PATH])

    def _get_template_path(self, config_parser: ConfigParser,
                           note_type: int) -> Path:
        templates_dir_path = \
            Path(config_parser[CONF_SEC_GENERAL][CONF_FIELD_TEMPLATE_REL_DIR])
        template_name_str = \
            config_parser[CONF_SEC_TEMPLATE_NAMES][NOTE_TYPES[note_type]]
        return self.zettel_path / templates_dir_path / template_name_str

    def _get_write_dir_path(self, config_parser: ConfigParser,
                            note_type: int) -> Path:
        dir_name = \
            config_parser[CONF_SEC_NOTE_DIR_NAMES][NOTE_TYPES[note_type]]
        return self.zettel_path.joinpath(dir_name)

    def _check_config_sections_exist(self, config_parser,
                                     default_parser) -> int:
        # check if all sections exist in config file
        for sec in default_parser.sections():
            if not config_parser.has_section(sec):
                return ErrorResponse(CONFIG_ERROR,
                                     'Config file missing section:   ' + sec)
        return ErrorResponse(SUCCESS, '')

    def _check_config_options_exist(self, config_parser,
                                    default_parser) -> int:
        # check if all options exist in config file
        for sec in default_parser.sections():
            for opt in default_parser.options(sec):
                if not config_parser.has_option(sec, opt):
                    msg = 'Config file missing option   ' + opt + '   '
                    msg += 'under section   ' + sec
                    return ErrorResponse(CONFIG_ERROR,
                                         msg)
        return ErrorResponse(SUCCESS, '')

    def _check_config_directories_exist(self, config_parser,
                                        default_parser) -> int:
        # check if zettel path exists
        z_path = Path(config_parser[CONF_SEC_GENERAL][CONF_FIELD_ZETTEL_PATH])
        if not z_path.is_dir():
            return ErrorResponse(PATH_ERROR,
                                 'Zettel path not valid: ' + str(z_path))
        # check if template path exists
        t_path = z_path.joinpath(
            config_parser[CONF_SEC_GENERAL][CONF_FIELD_TEMPLATE_REL_DIR]
        )
        if not t_path.is_dir():
            return ErrorResponse(PATH_ERROR,
                                 'Template path not valid: ' + str(t_path))
        # check if target note path exists
        for note_type in \
                config_parser.options(CONF_SEC_NOTE_DIR_NAMES):
            dir_name = config_parser[CONF_SEC_NOTE_DIR_NAMES][note_type]
            dir_path = z_path.joinpath(dir_name)
            if not dir_path.is_dir():
                return ErrorResponse(PATH_ERROR,
                                     'Write destination not found: ' +
                                     str(dir_path))
        return ErrorResponse(SUCCESS, '')

    def _check_config_files_exist(self, config_parser,
                                  default_parser) -> int:
        z_path = Path(config_parser[CONF_SEC_GENERAL][CONF_FIELD_ZETTEL_PATH])
        t_path = z_path.joinpath(
            config_parser[CONF_SEC_GENERAL][CONF_FIELD_TEMPLATE_REL_DIR]
        )
        # check if template files exist
        for note_type in \
                config_parser.options(CONF_SEC_TEMPLATE_NAMES):
            file_name = config_parser[CONF_SEC_TEMPLATE_NAMES][note_type]
            file_path = t_path.joinpath(file_name)
            if not file_path.is_file():
                return ErrorResponse(PATH_ERROR,
                                     'Template file not found: ' +
                                     str(file_path))
        return ErrorResponse(SUCCESS, '')

    def check_config_parser(self, config_parser,
                            default_parser) -> int:
        c, d = config_parser, default_parser
        for check_func in [self._check_config_sections_exist,
                           self._check_config_options_exist,
                           self._check_config_directories_exist,
                           self._check_config_files_exist]:
            err_resp = check_func(c, d)
            if err_resp.error != SUCCESS:
                return err_resp
        return ErrorResponse(SUCCESS, '')

    def _read_config(self, config_path: Path) -> ConfigParser:
        config_parser = ConfigParser()
        config_parser.read(config_path)
        return config_parser

