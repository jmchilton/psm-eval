from yaml import load
from optparse import OptionParser

ARG_PROPERTIES = ['psms', 'psms_type', 'output']

def load_settings():
    option_parser = __option_parser()

    (options, _) = option_parser.parse_args()

    settings_path = "./settings.yaml"

    settings = __read_yaml(settings_path)
 
    # ARG_PROPERTIES contains command-line arguments that will
    # override defaults in settings, do this override for each
    # property (if needed).
    for property in ARG_PROPERTIES:
        __copy_arg_to_options(settings, options, property)

    __preprocess(settings)

    return settings


def __option_parser():
    """

    >>> parser = __option_parser()
    >>> from shlex import split
    >>> def options(str): return parser.parse_args(split(str))[0]
    >>> opts = options("--settings /path/to/settings.yaml")
    >>> opts.settings
    '/path/to/settings.yaml'
    """
    parser = OptionParser()
    parser.add_option("--psms", default=None)
    parser.add_option("--psms_type", default=None)
    parser.add_option("--output", default=None)  # defauts to stdout
    parser.add_option("--settings")
    return parser


def __copy_arg_to_options(options, args, property):
    arg_property = getattr(args, property)
    if arg_property or not property in options:
        options[property] = arg_property


def __read_yaml(yaml_file):
    with open(yaml_file) as in_handle:
        return load(in_handle)


def __preprocess(settings):
    """
    Preprocess raw settings read in from YAML file and resolve references.

    >>> settings = {"ions_defs": {"moo": {"series": ["y1"]}}, "columns": [{"ions_ref": "moo"}]}
    >>> __preprocess(settings)
    >>> settings["columns"][0]["ions"]["series"]
    ['y1']
    >>> settings = {"peak_filter_defs": {"top_half": {"type": 'quantile'}}, "columns": [{"peak_filters": [{"peak_filter_ref": "top_half"}]}]}
    >>> __preprocess(settings)
    >>> settings["columns"][0]["peak_filters"][0]["type"]
    'quantile'
    >>> settings = {"columns": [{"ions": {"series": "b1,y1"}}]}  # Check list expansion
    >>> __preprocess(settings)
    >>> settings["columns"][0]["ions"]["series"][0]
    'b1'
    >>> settings["columns"][0]["ions"]["series"][1]
    'y1'
    >>> settings = {"columns": [{"ions": {"series": ["b1","y1"]}}]}  #Ensure preprocessing doesn't break preexpanded properties.
    >>> __preprocess(settings)
    >>> settings["columns"][0]["ions"]["series"][0]
    'b1'
    >>> settings["columns"][0]["ions"]["series"][1]
    'y1'
    >>> settings = {"peak_list": "/home/moo"}
    >>> __preprocess(settings)
    >>> settings["peak_lists"][0]
    '/home/moo'
    """
    ions_defs = settings.get("ions_defs", {})
    __yaml_replace(settings, "ions_ref", "ions", ions_defs)
    peak_filter_defs = settings.get("peak_filter_defs", {})
    __yaml_replace(settings, "peak_filter_ref", None, peak_filter_defs)
    __yaml_expand_list(settings, 'series')
    __yaml_expand_list(settings, 'losses')
    for key, value in dict(settings).iteritems():
        if key == "peak_list":
            del settings[key]
            settings["peak_lists"] = [value]


def __yaml_expand_list(data, list_key):
    if hasattr(data, 'iteritems'):
        for key, value in dict(data).iteritems():
            if key == list_key and (isinstance(value, str) or isinstance(value, unicode)):
                data[key] = [v.strip() for v in value.split(",")]
            else:
                __yaml_expand_list(value, list_key)
    elif isinstance(data, list):
        for value in data:
            __yaml_expand_list(value, list_key)


def __yaml_replace(data, replacement_key, replacing_key, replacements):
    if hasattr(data, 'iteritems'):
        for key, value in dict(data).iteritems():
            if key == replacement_key:
                replacement_value = replacements[value]
                if replacing_key:
                    data[replacing_key] = replacement_value
                else:
                    data.update(replacement_value)
                del data[replacement_key]
            else:
                __yaml_replace(value, replacement_key, replacing_key, replacements)
    elif isinstance(data, list):
        for value in data:
            __yaml_replace(value, replacement_key, replacing_key, replacements)
