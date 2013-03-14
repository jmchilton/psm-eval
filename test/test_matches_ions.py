from util import PsmeTestCase

from psme.column.matches_ions import MatchesIons


class MatchesIonsTestCase(PsmeTestCase):

    def test_mass_tolerance(self):
        matcher = MatchesIons()
        matcher._setup_ion_matcher({}, mass_tolerance=0.5)
        mock_ions = [_MockIon(100.0), _MockIon(102.0)]
        mock_peaks = [(100.4, 700.0), (200.1, 600.0)]
        matched_array = matcher._ions_matched(mock_ions, mock_peaks)
        self.assertTrue(matched_array[0])
        self.assertFalse(matched_array[1])

        # Local options override global settings
        matcher = MatchesIons()
        matcher._setup_ion_matcher({"mass_tolerance": 0.5}, mass_tolerance=0.1)
        matched_array = matcher._ions_matched(mock_ions, mock_peaks)
        self.assertFalse(matched_array[0])
        self.assertFalse(matched_array[1])

        # Global settings used if local mass_tolerance not specified.
        matcher = MatchesIons()
        matcher._setup_ion_matcher({"mass_tolerance": 0.5})
        matched_array = matcher._ions_matched(mock_ions, mock_peaks)
        self.assertTrue(matched_array[0])
        self.assertFalse(matched_array[1])


class _MockIon(object):

    def __init__(self, mz):
        self.mz = mz

    def get_mz(self):
        return self.mz
