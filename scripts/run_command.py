"""Entry point for main developer script.

Usage: python scripts/run_command.py -h

"""

import argparse
import json
import logging
import os
import subprocess
import sys

import init_path
from pyelect import htmlgen
from pyelect import jsongen
from pyelect import lang
from pyelect import utils


_DEFAULT_OUTPUT_DIR_NAME = '_build'
_FORMATTER_CLASS = argparse.RawDescriptionHelpFormatter


def get_default_sample_html_path():
    return os.path.join(_DEFAULT_OUTPUT_DIR_NAME, 'sample.html')


def command_lang_make_auto(ns):
    path = ns.input_path
    lang.create_auto_translations(path)


def command_lang_make_ids(ns):
    path = ns.input_path
    data = lang.create_text_ids(path)
    print(utils.yaml_dump(data))


def command_make_json(ns):
    path = ns.output_path

    data = jsongen.make_all_data()
    text = json.dumps(data, indent=4, sort_keys=True)
    print("JSON:\n{0}".format(text))
    utils.write(path, text)


def command_parse_csv(ns):
    path = ns.path
    data = lang.parse_contest_csv(path)
    print(data)


def command_sample_html(ns):
    path = ns.output_path
    if path is None:
        path = os.path.join(utils.get_repo_dir(), get_default_sample_html_path())
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    # Load JSON data.
    json_path = utils.get_default_json_path()
    with open(json_path) as f:
        input_data = json.load(f)
    # Make and output HTML.
    html = htmlgen.make_html(input_data)
    with open(path, "w") as f:
        f.write(html)
    subprocess.call(["open", path])
    print(html)


def command_yaml_normalize(ns):
    path = ns.path
    data = utils.read_yaml(path)
    utils.write_yaml(data, path, stdout=True)


def command_yaml_update_lang(ns):
    path = ns.path
    data = utils.read_yaml(path)
    utils.write_yaml(data, path, stdout=True)


def make_subparser(sub, command_name, command_func, help, details=None, **kwargs):
    # Capitalize the first letter for the long description.
    desc = help[0].upper() + help[1:]
    if details is not None:
        desc += "\n\n{0}".format(details)
    parser = sub.add_parser(command_name, formatter_class=_FORMATTER_CLASS,
                            help=help, description=desc, **kwargs)
    parser.set_defaults(run_command=command_func)
    return parser


def create_parser():
    """Return an ArgumentParser object."""
    root_parser = argparse.ArgumentParser(formatter_class=_FORMATTER_CLASS,
            description="command script for repo contributors")
    sub = root_parser.add_subparsers(help='sub-command help')

    parser = make_subparser(sub, "lang_make_auto", command_lang_make_auto,
                help="make the automated translations from a CSV file.")
    parser.add_argument('input_path', metavar='CSV_PATH',
        help="a path to a CSV file.")

    parser = make_subparser(sub, "lang_make_ids", command_lang_make_ids,
                help="create text ID's from a CSV file.")
    parser.add_argument('input_path', metavar='CSV_PATH',
        help="a path to a CSV file.")

    default_output = utils.REL_PATH_JSON
    parser = make_subparser(sub, "make_json", command_make_json,
                help="create or update a JSON data file.")
    parser.add_argument('output_path', metavar='PATH', nargs="?", default=default_output,
        help=("the output path. Defaults to the following path relative to the "
              "repo root: {0}.".format(default_output)))

    parser = make_subparser(sub, "parse_csv", command_parse_csv,
                help="parse a CSV language file from the Department.")
    parser.add_argument('path', metavar='PATH', help="a path to a CSV file.")

    parser = make_subparser(sub, "sample_html", command_sample_html,
                help="make sample HTML from the JSON data.",
                details="Uses the repo JSON file as input.")
    parser.add_argument('output_path', metavar='PATH', nargs="?",
        help=("the output path. Defaults to the following relative to the repo: {0}"
              .format(get_default_sample_html_path())))

    parser = make_subparser(sub, "yaml_norm", command_yaml_normalize,
                help="normalize a YAML file.")
    parser.add_argument('path', metavar='PATH', help="a path to a YAML file.")

    parser = make_subparser(sub, "yaml_update_lang", command_yaml_update_lang,
                help="update a YAML translation file from the English.")
    parser.add_argument('path', metavar='PATH',
        help="the target path of a non-English YAML file.")

    return root_parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    logging.basicConfig(level='INFO')
    parser = create_parser()
    ns = parser.parse_args(argv)
    try:
        ns.run_command
    except AttributeError:
        # We need to handle this exception because of the following
        # behavior change:
        #   http://bugs.python.org/issue16308
        parser.print_help()
    else:
        ns.run_command(ns)


if __name__ == '__main__':
    main()
