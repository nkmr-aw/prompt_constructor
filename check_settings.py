# -*- coding: utf-8 -*-
from cerberus import Validator


def sanitize_input(value, data_type):
    if data_type == 'str':
        return str(value).strip()
    elif data_type == 'int':
        try:
            return int(value)
        except ValueError:
            return None
    elif data_type == 'float':
        try:
            return float(value)
        except ValueError:
            return None
    elif data_type == 'bool':
        if value.lower() == 'enable':
            return True
        elif value.lower() == 'disable':
            return False
        else:
            return None
    else:
        return value


def validate_settings(settings):
    schema = {
        'lang': {'type': 'string', 'allowed': ['en', 'ja'], 'required': True},
        'increment_unit': {'type': 'float', 'allowed': [0.05, 0.1], 'required': True},
        'window_width': {'type': 'integer', 'min': 1, 'required': True},
        'window_height': {'type': 'integer', 'min': 1, 'required': True},
        'itemarea_displines': {'type': 'integer', 'min': 1, 'max': 20, 'required': True},
        'scroll_lines': {'type': 'integer', 'min': 1, 'max': 20, 'required': True},
        'messages': {'type': 'string', 'allowed': ['enable', 'disable'], 'required': True},
        'autosave_json': {'type': 'string', 'allowed': ['enable', 'disable'], 'required': True},
        'backup_json': {'type': 'string', 'allowed': ['enable', 'disable'], 'required': True},
        'textfont': {'type': 'string', 'regex': r'^(?!.*[;&|`\$]).*$', 'required': True},
        'fontsize_treeview': {'type': 'integer', 'min': 8, 'max': 32, 'required': True},
        'fontsize_textbox': {'type': 'integer', 'min': 8, 'max': 32, 'required': True},
        'datetime_format': {'type': 'string', 'regex': r'^[%Y%m%d%H%M%S_.-]+$', 'required': True},
        'multiple_boot': {'type': 'string', 'allowed': ['enable', 'disable'], 'required': True},
    }

    validator = Validator(schema)
    if validator.validate(settings):
        return True, {}
    else:
        return False, validator.errors



