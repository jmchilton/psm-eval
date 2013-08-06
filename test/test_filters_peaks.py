from util import PsmeTestCase

from psme.column.filters_peaks import FiltersPeaks


class FiltersPeaksTestCase(PsmeTestCase):

    def test_peaks(self):
        peaks = self._filter_scan()
        self._assert_peak_is(peaks[0], 149.1203003, 1.883338094)
        self._assert_peak_is(peaks[-1], 479.9738159, 2.316269875)

    def test_mz_range(self):
        peaks = self._filter_scan({"peak_filters": [{"type": "mz_range_absolute", "min": 275.0, "max": 300.0}]})
        self._assert_peak_is(peaks[0], 281.3802795, 1.877650738)
        self._assert_peak_is(peaks[-1], 299.9325562, 1.883962154)

    def test_intensity_range(self):
        peaks = self._filter_scan({"peak_filters": [{"type": "intensity_range", "min": 10.0, "max": 12.0}]})
        self._assert_peak_is(peaks[0], 327.836792, 10.00239944)
        self._assert_peak_is(peaks[-1], 355.4126282, 11.12517834)

    def test_base_peak_mz(self):
        # 479.9738155/354.541259765625
        # 1.3537883173803076

        # 149.1203003/354.541259765625
        # 0.42060069510267517
        peaks = self._filter_scan({"peak_filters": [{"type": "mz_range_percent_bp", "min": .42, "max": 1.4}]})
        self.assertAlmostEqual(peaks[0][0], 149.1203003, 4)
        self.assertAlmostEqual(peaks[-1][0], 479.9738155, 4)
        peaks = self._filter_scan({"peak_filters": [{"type": "mz_range_percent_bp", "min": .43, "max": 1.3}]})
        self.assertNotAlmostEqual(peaks[0][0], 149.1203003, 4)
        self.assertNotAlmostEqual(peaks[-1][0], 479.9738155, 4)

    def test_intensity_percent(self):
        # Most intense peak has intensity of  58.05626678...
        # second has 13.014031 (around 22%)
        peaks = self._filter_scan({"peak_filters": [{"type": "percent_max_intensity", "percent": .23}]})
        assert len(peaks) == 1
        peaks = self._filter_scan({"peak_filters": [{"type": "percent_max_intensity", "percent": .21}]})
        assert len(peaks) > 1

    def _assert_peak_is(self, peak, expected_mz, expected_intensity):
        (mz, intensity) = peak
        self.assertAlmostEquals(expected_mz, mz, 4)
        self.assertAlmostEquals(expected_intensity, intensity, 4)

    def _filter_scan(self, options={}, scan=None):
        filters_peaks = self._setup_filter(options)
        if scan == None:
            scan = self._test2_first_scan()
        return filters_peaks._filtered_peaks(scan)

    def _setup_filter(self, options={}):
        filters_peaks = FiltersPeaks()
        filters_peaks._setup_peak_filters(**options)
        return filters_peaks
