
from collections import defaultdict
import glob
import json
import os
from pprint import pprint

from pyelect import lang
from pyelect import utils


COURT_OF_APPEALS_ID = 'ca_court_app'

KEY_DISTRICTS = 'districts'
KEY_ID = '_id'
KEY_OFFICES = 'offices'


def dd_dict():
    """A factory function that returns a defaultdict(dict)."""
    return defaultdict(dict)


def path_to_langcode(path):
    """Extract the language code from a path and return it."""
    head, tail = os.path.split(path)
    base, ext = os.path.splitext(tail)
    return base


def yaml_to_words(data, lang):
    """Return a dict from: text_id to word in the given language."""
    text_node = data['texts']
    # Each trans_map is a dict from: language code to translation.
    words = {text_id: trans_map[lang] for text_id, trans_map in text_node.items()}
    return words


def read_phrases(path):
    """Read a file, and return a dict of: text_id to translation."""
    lang_code = path_to_langcode(path)
    yaml_data = utils.read_yaml(path)
    words = yaml_to_words(yaml_data, lang_code)
    return lang_code, words


def read_lang_dir(dir_name):
    lang_dir = lang.get_lang_dir()
    auto_dir = os.path.join(lang_dir, lang.DIR_LANG_AUTO)
    glob_path = os.path.join(auto_dir, "*.yaml")
    paths = glob.glob(glob_path)

    data = defaultdict(dd_dict)
    for path in paths:
        lang_code, phrases = read_phrases(path)
        for text_id, phrase in phrases.items():
            data[text_id][lang_code] = phrase

    return data


def get_language_codes():
    dir_path = utils.get_lang_dir()
    langs = []
    for path in paths:
        head, tail = os.path.split(path)
        base, ext = os.path.splitext(tail)
        langs.append(base)
    return langs


def get_yaml(name):
    data_dir = utils.get_pre_data_dir()
    path = "{0}.yaml".format(os.path.join(data_dir, name))
    return utils.read_yaml(path)


def add_source(data, source_name):
    source_data = get_yaml(source_name)
    for key, value in source_data.items():
        data[key] = value


def make_node_i18n():
    """Return the node containing internationalized data."""
    data = read_lang_dir('auto')
    return data


def make_court_of_appeals_division_numbers():
    return range(1, 6)


def make_court_of_appeals_district_id(division):
    return "{0}_d1_div{1}".format(COURT_OF_APPEALS_ID, division)


def make_court_of_appeals_office_type_id(office_type):
    return "{0}_{1}".format(COURT_OF_APPEALS_ID, office_type)


def make_court_of_appeals_office_id(division, office_type):
    return "{0}_d1_div{1}_{2}".format(COURT_OF_APPEALS_ID, division, office_type)


def make_court_of_appeals_district(division):
    _id = make_court_of_appeals_district_id(division)
    district = {
        KEY_ID: _id,
        'district_type_id': 'ca_court_app_d1',
        'district_code': division,
    }
    return district


def make_court_of_appeals_districts():
    districts = [make_court_of_appeals_district(c) for c in
                 make_court_of_appeals_division_numbers()]
    return districts


def make_court_of_appeals_office(division, office_type, seat_count=None):
    office = {
        KEY_ID: make_court_of_appeals_office_id(division, office_type),
        'office_type_id': make_court_of_appeals_office_type_id(office_type),
    }
    if seat_count is not None:
        office['seat_count'] = seat_count

    return office


def make_court_of_appeals():
    keys = (KEY_DISTRICTS, KEY_OFFICES)
    # TODO: make the following two lines into a helper function.
    data = {k: [] for k in keys}
    districts, offices = [data[k] for k in keys]

    division_numbers = make_court_of_appeals_division_numbers()
    for division in division_numbers:
        office = make_court_of_appeals_office(division, 'pj')
        offices.append(office)
        office = make_court_of_appeals_office(division, 'aj', seat_count=3)
        offices.append(office)

    return offices


def add_node(data, node_name):
    make_node_function_name = "make_node_{0}".format(node_name)
    make_node = globals()[make_node_function_name]
    node = make_node()
    data[node_name] = node


def make_all_data():
    data ={}

    add_node(data, 'i18n')
    add_source(data, 'offices')

    return data
    add_source(data, 'bodies')
    add_source(data, 'district_types')
    add_source(data, 'office_types')

    # Make districts.
    districts = make_court_of_appeals_districts()
    data['districts'] = districts

    offices = make_court_of_appeals()
    data['court_offices'] = offices

    return data
