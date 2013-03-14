from psme.column import build_column_provider
from util import PsmeTestCase

from psme.peak_list import mzml_spectrum_to_scan


class StatisticsTestCase(PsmeTestCase):

    def test_total_ion_current(self):
        spectra = mzml_spectrum_to_scan(list(self._read_test_mzml())[0], None, 0)
        stat = build_column_provider({}, "total_ion_current")
        value = stat.calculate(spectra, None)
        self.assertEquals(9849353.0, value)

    def test_num_matching_peaks(self):
        spectra = mzml_spectrum_to_scan(list(self._read_test_mzml())[0], None, 0)
        stat = build_column_provider({}, "num_peaks")
        value = stat.calculate(spectra, None)
        self.assertEquals(1480, value)
