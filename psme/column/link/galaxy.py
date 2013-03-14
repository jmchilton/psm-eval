from urllib import quote


class LinkBuilder(object):
    """
    Builds protvis links routed through Galaxy. See Galaxy-P for an example
    of how to configure Galaxy to handle this:

    https://bitbucket.org/galaxyp/cloud-galaxyp-central
    """

    def __init__(self, **builder_settings):
        # Default - build relative link
        galaxy_url = quote(builder_settings.get('galaxy_url', ''))
        controller = quote(builder_settings.get('controller', '/dataset/display_application'))
        app_name = quote(builder_settings.get('app_name', 'protvis_mzml'))
        link_name = quote(builder_settings.get('link_name', 'ProtVis'))
        link_prefix_template = "%s%s?user_id=None&app_name=%s&link_name=%s"
        link_prefix_params = (galaxy_url, controller, app_name, link_name)
        self.link_prefix = link_prefix_template % link_prefix_params

    def get_link(self, scan, psm):
        spectrum = quote(self.__spectrum_rep(scan))
        peptide = quote(self.__peptide_rep(psm))
        dataset_id = quote(self.__dataset_id(scan))
        link_template = "%s&dataset_id=%s&app_spectrum=%s&app_peptide=%s"
        link = link_template % (self.link_prefix, dataset_id, spectrum, peptide)
        return link

    def __spectrum_rep(self, scan):
        return str(scan.index)

    def __peptide_rep(self, psm):
        return str(psm.peptide.sequence)

    def __dataset_id(self, scan):
        return scan.source.encoded_id
