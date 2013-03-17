from urllib import quote
from re import search

from psme.column.link import find_link_builder
from util import PsmeTestCase

from psme.peak_list import ScanSource, Scan
from psme.psm import Psm
from psme.peptide import Peptide


class PeakListTestCase(PsmeTestCase):

    def test_galaxy_links(self):
        galaxy_link_builder = find_link_builder(link_type="galaxy")
        source_options = {"path": "/test/path", "encoded_id": "12356abcd"}
        test_scan_source = ScanSource(0, source_options)
        test_index = 55
        test_scan = Scan(test_scan_source, test_index, mz_array=None, intensity_array=None)
        test_peptide = Peptide(sequence="SAMPLER", modifications=[{"position": 1, "mod_mass": 10.0}], n_term_modifications=[54])
        test_psm = Psm(None, test_peptide)
        link = galaxy_link_builder.get_link(test_scan, test_psm)
        url = link.url
        peptide = quote("SAMPLER;%f@n;%f@2" % (54.0, 10.0))
        expected_url = \
            "/dataset/display_application?user_id=None&app_name=protvis_mzml&link_name=ProtVis&dataset_id=12356abcd&app_spectrum=55&app_peptide=%s" % peptide
        self.assertEquals(expected_url, url)
        label = link.label
        match = search("peptide (.*) on", label)
        peptide_label = match.group(1)
        self.assertTrue(peptide_label.startswith("SAMPLER"), peptide_label)
        rest_label = peptide_label[len("SAMPLER"):]
        self.assertTrue(rest_label == " (with modifications 54 @ N terminal, 10 @ 2)")
