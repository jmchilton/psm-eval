from unittest import TestCase
from pyteomics.mzml import read as mzml_read
from os.path import join, pardir, dirname
from psme.peptide import Peptide, PeptideContext
from psme.peak_list import ScanSource, mzml_spectrum_to_scan
from psme.ion import get_ions

TEST_PEPTIDE_SAMPLER = Peptide("SAMPLER")
TEST_PEPTIDE_CONTEXT_AMP = PeptideContext(TEST_PEPTIDE_SAMPLER, start=1, stop=4)
TEST_PEPTIDE_CONTEXT_SAMPLER = PeptideContext(TEST_PEPTIDE_SAMPLER, start=0, stop=7)


class PsmeTestCase(TestCase):

    def _read_test2_mzxml(self):   # TODO: Rename
        return self._read_test_mzml('test2.mzML')

    def _test2_first_scan(self):
        return mzml_spectrum_to_scan(self._read_test2_mzxml().next(), None, 0)

    def _read_test_mzml(self, name='test.mzML'):
        return mzml_read(self._test_data_path(name))

    def _test_data_path(self, filename):
        return join(dirname(__file__), pardir, "test-data", filename)

    def _load_test_psms(self, loader_cls, test_data, settings={}, source_manager=None, source_statistics=[]):
        if source_manager == None:
            source_manager = TestScanSourceManager()
        loader = loader_cls(settings, source_manager)
        test_path = self._test_data_path(test_data)
        return loader.load(test_path, source_statistics)


class TestScanSourceManager():

    def __init__(self, test_scan_source=None):
        if test_scan_source == None:
            test_scan_source = ScanSource(0, "/path/to/test.mzML")
        self.test_scan_source = test_scan_source

    def match_by_name(self, id):
        return self.test_scan_source

    def match_by_index(self, index):
        return self.test_scan_source


def get_b1_ions(peptide, **calc_args):
    return get_ions(peptide=peptide, calc_args=calc_args, **{"series": ["b1"]})
