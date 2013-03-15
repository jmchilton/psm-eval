from re import match


def find_link_builder(**builder_settings):
    """
    """
    link_builder_type = builder_settings["link_type"]
    if not match("\w+", link_builder_type):
        raise Exception("Invalid link type specified [%s]" % link_builder_type)
    link_builder_module_name = "%s.%s" % (__name__, link_builder_type)
    #builder_class = builder_settings.get("builder_class", "LinkBuilder")
    link_builder_module = \
        __import__(link_builder_module_name, fromlist=['LinkBuilder'])
    return link_builder_module.LinkBuilder(**builder_settings)


class Link(object):

    value_type = "link"

    def __init__(self, url, label):
        self.url = url
        self.label = label
