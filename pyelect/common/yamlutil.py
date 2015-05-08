
import logging
import os

import yaml

from pyelect.common import utils


KEY_META_COMMENTS = 'comments'
KEY_META = '_meta'
KEY_META_COMMENTS = 'comments'
KEY_FILE_TYPE = '_type'
KEY_FILE_TYPE_COMMENT = '_type_comment'

_log = logging.getLogger()


# The idea for this comes from here:
# http://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
def _yaml_str_representer(dumper, data):
    """A PyYAML representer that uses literal blocks for multi-line strings.

    For example--

      long: |
        This is
        a multi-line
        string.
      short: This is a one-line string.
    """
    style = '|' if '\n' in data else None
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=style)


# TODO: is there a way to configure this within a function as opposed to
#   at the module level?
yaml.add_representer(str, _yaml_str_representer)


def read_yaml(path):
    with open(path) as f:
        data = yaml.load(f)
    return data


def read_yaml_rel(rel_path, file_base=None, key=None):
    """Return the data in a YAML file as a Python dict.

    Arguments:
      rel_path: the path to the file relative to the repo root.
      key: optionally, the key-value to return.
    """
    if file_base is not None:
        file_name = "{0}.yaml".format(file_base)
        rel_path = os.path.join(rel_path, file_name)

    repo_dir = utils.get_repo_dir()
    path = os.path.join(repo_dir, rel_path)

    data = read_yaml(path)
    if key is not None:
        data = data[key]

    return data


def yaml_dump(*args):
    return yaml.dump(*args, default_flow_style=False, allow_unicode=True, default_style=None)


def _write_yaml(data, path, stdout=None):
    if stdout is None:
        stdout = False
    with open(path, "w") as f:
        yaml_dump(data, f)
    if stdout:
        print(yaml_dump(data))


def get_yaml_meta(data):
    return utils.get_required(data, KEY_META)


def _get_yaml_file_type_from_meta(meta):
    file_type = get_required(meta, KEY_FILE_TYPE)
    if file_type not in FILE_TYPES:
        raise Exception('bad file type: {0}'.format(file_type))
    return file_type


def _get_yaml_file_type(data):
    meta = get_yaml_meta(data)
    file_type = _get_yaml_file_type_from_meta(meta)
    return file_type


def _set_header(data, file_type, comments=None):
    meta = data.setdefault(KEY_META, {})

    if file_type is None:
        # Then we require that the file type already be specified.
        file_type = _get_yaml_file_type_from_meta(meta)
    else:
        meta[KEY_FILE_TYPE] = file_type

    comment = FILE_TYPE_COMMENTS.get(file_type)
    if comment:
        meta[KEY_FILE_TYPE_COMMENT] = comment

    if comments is not None:
        meta[KEY_META_COMMENTS] = comments


def write_yaml_with_header(data, rel_path, file_type=None, comments=None,
                           stdout=None):
    repo_dir = utils.get_repo_dir()
    path = os.path.join(repo_dir, rel_path)
    _set_header(data, file_type=file_type, comments=comments)
    _write_yaml(data, path, stdout=stdout)


def _is_yaml_normalizable(data, path_hint):
    try:
        file_type = _get_yaml_file_type(data)
    except:
        raise Exception("for file: {0}".format(path_hint))
    # Use a white list instead of a black list to be safe.
    return file_type in (FILE_AUTO_UPDATED, FILE_AUTO_GENERATED)


def is_yaml_file_normalizable(path):
    data = read_yaml(path)
    return _is_yaml_normalizable(data, path_hint=path)


def normalize_yaml(path, stdout=None):
    data = read_yaml(path)
    normalizable = _is_yaml_normalizable(data, path_hint=path)
    if not normalizable:
        _log.info("skipping normalization: {0}".format(path))
        return

    write_yaml_with_header(data, path, stdout=stdout)