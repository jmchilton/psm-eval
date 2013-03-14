

class PepXmlLoader(object):
    """
    Placeholder for the yet to be implemented PepXml PSM loader.
    """
    def __init__(self, settings, scan_source_manager):
        self.settings = settings
        self.scan_source_manager = scan_source_manager

    def load(self, f, source_statistic_names):
        raise NotImplementedError()
