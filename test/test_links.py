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
        test_peptide = Peptide(sequence="SAMPLER")
        test_psm = Psm(None, test_peptide)
        url = galaxy_link_builder.get_link(test_scan, test_psm)
        expected_url = \
            "/dataset/display_application?user_id=None&app_name=protvis_mzml&link_name=ProtVis&dataset_id=12356abcd&app_spectrum=55&app_peptide=SAMPLER"
        self.assertEquals(expected_url, url)
