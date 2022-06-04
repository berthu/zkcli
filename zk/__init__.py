"""Top-level package for zk"""
# zk/__init__.py

__app_name__ = "zk"
__version__ = "1.0"

CONFIG_FILE_NAME = '.zkcli'

DEFAULT_EDITOR = 'vim'

(
    SUCCESS,
    WRITE_ERROR,
    READ_ERROR,
    CONFIG_ERROR,
    PATH_ERROR
) = range(5)

ERRORS = {
    WRITE_ERROR: 'write error',
    READ_ERROR: 'template read error',
    CONFIG_ERROR: 'config read error',
    PATH_ERROR: 'path error',
}

(
    FLEETING,
    DAILY,
    MEETING,
    LITERATURE,
    PERMANENT,
    TEMPLATES,
) = range(6)

NOTE_TYPES = {
    FLEETING: 'fleeting',
    LITERATURE: 'literature',
    DAILY: 'daily',
    MEETING: 'meeting',
    PERMANENT: 'permanent',
}

DEFAULT_FOLDERS = {
    FLEETING: 'Fleeting',
    DAILY: 'Fleeting',
    MEETING: 'Fleeting',
    LITERATURE: 'Literature',
    PERMANENT: 'Permanent',
    TEMPLATES: '.Templates'
}

DEFAULT_TEMPLATE_NAMES = {
    FLEETING: 'fleetingYYMMDD-HHMMtopic.md',
    LITERATURE: 'literature.md',
    DAILY: 'dailyYYMMDD.md',
    MEETING: 'meetingYYMMDDtopic.md',
    PERMANENT: 'permanent.md',
}

CONF_SEC_GENERAL = 'General'
CONF_FIELD_ZETTEL_PATH = 'ZettelkastenPath'
CONF_FIELD_TEMPLATE_REL_DIR = 'TemplatesDirectory'
CONF_SEC_TEMPLATE_NAMES = 'Template Names'
CONF_SEC_NOTE_DIR_NAMES = 'Note Destination Directory Names'
