from urllib import quote
from psme.column.link import Link


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
        self.kwds = builder_settings

    def get_link(self, scan, psm):
        spectrum = quote(self.__spectrum_rep(scan))
        peptide = quote(self.__peptide_rep(psm))
        peptide_label = self.__peptide_label(psm)
        dataset_id = quote(self.__dataset_id(scan))
        link_template = "%s&dataset_id=%s&app_spectrum=%s&app_peptide=%s"
        link_url = link_template % (self.link_prefix, dataset_id, spectrum, peptide)
        return Link(url=link_url, label="View peptide %s on spectrum %s" % (peptide_label, spectrum))

    def __spectrum_rep(self, scan):
        return str(scan.index)

    def __peptide_rep(self, psm):
        peptide = psm.peptide
        sequence = peptide.sequence
        rep = str(sequence)
        if peptide.n_term_modifications:
            rep += ";%f@n" % peptide.sum_of_modifications("n", **self.kwds)
        if peptide.c_term_modifications:
            rep += ";%f@c" % peptide.sum_of_modifications("c", **self.kwds)
        for i, modifications in enumerate(peptide.modifications):
            if modifications:
                rep += ";%f@%d" % (peptide.sum_of_modifications(i, **self.kwds), i + 1)
        return rep

    def __peptide_label(self, psm):
        peptide = psm.peptide
        modifications_label = self.__peptide_modifications_label(peptide)
        return "%s%s" % (peptide.sequence, "" if not modifications_label else " (with modifications %s)" % modifications_label)

    def __peptide_modifications_label(self, peptide):
        rep = ""

        def append_rep(str, rest):
            return "%s%s" % (("%s, " % str) if str else "", rest)

        for modification in peptide.n_term_modifications:
            rep = append_rep(rep, "%s @ N terminal" % self.__format_decimal(peptide.modification_mass(modification, **self.kwds)))
        for modification in peptide.c_term_modifications:
            rep = append_rep(rep, "%s @ C terminal" % self.__format_decimal(peptide.modification_mass(modification, **self.kwds)))
        for i, modification_list in enumerate(peptide.modifications):
            for modification in modification_list:
                rep = append_rep(rep, "%s @ %d" % (self.__format_decimal(peptide.modification_mass(modification, **self.kwds)), i + 1))
        return rep

    def __format_decimal(self, number):
        return ('%f' % number).rstrip('0').rstrip('.')

    def __dataset_id(self, scan):
        return scan.source.encoded_id
