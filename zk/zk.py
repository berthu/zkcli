#!/usr/bin/env python3
"""This module provides the zk controller."""
# zk/zk.py
__author__ = "Bert Hu"
__copyright__ = "Copyright 2022"
__credits__ = ["Bert Hu"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Bert Hu"
__email__ = ""
__status__ = "Production"


from pathlib import Path
from datetime import datetime
from zk.config import ZettelConfig


class Librarian:
    def __init__(self, zk_config: ZettelConfig) -> None:
        self.zettel_path = zk_config.zettel_path
        # the following objects are dicts of DocumentPath NamedTuples
        self.template_paths = zk_config.template_paths
        self.write_dir_paths = zk_config.write_dir_paths
        return

    def get_write_path(self, note_type: int, topic: str = '') -> Path:
        template_path = self.template_paths[note_type]
        write_dir_path = self.write_dir_paths[note_type]
        note_name = self.get_note_name(template_path.name, topic)
        note_path = write_dir_path.joinpath(note_name)
        return note_path

    def get_note_name(self, template_name: str, topic: str = '') -> str:
        replace_dict = {
            'YYYYMMDD': datetime.now().strftime('%Y%m%d'),
            'YYMMDD': datetime.now().strftime('%y%m%d'),
            'HHMMSS': datetime.now().strftime('%H%M%S'),
            'HHMM': datetime.now().strftime('%H%M'),
            'topic': topic,
            'permanent': topic,
            'literature': topic,
        }
        note_name = template_name
        for (placeholder, replace_str) in replace_dict.items():
            note_name = note_name.replace(placeholder, replace_str)
        return note_name

    def _sanitize(self, line_str: str, topic: str) -> str:
        replace_dict = {
            'YYYY-MM-DD A': datetime.now().strftime('%Y-%m-%d %A'),
            'YYYY-MM-DD': datetime.now().strftime('%Y-%m-%d'),
            'YYYYMMDD': datetime.now().strftime('%Y%m%d'),
            'YYMMDD': datetime.now().strftime('%y%m%d'),
            'HHMMSS': datetime.now().strftime('%H%M%S'),
            'HHMM': datetime.now().strftime('%H%M'),
            '%topic%': topic,
        }
        result = line_str
        for (placeholder, replace_str) in replace_dict.items():
            result = result.replace(placeholder, replace_str)
        return result

    def write_note(self, note_type: int, topic: str = '') -> str:
        template_path = self.template_paths[note_type]
        note_path = self.get_write_path(note_type, topic)
        with open(template_path, 'r') as template:
            with open(note_path, 'w') as note:
                for line in template:
                    note.write(self._sanitize(line, topic))
        return note_path
